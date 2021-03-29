#  Copyright (c) 2021.  Liquid Fortress. All rights reserved.
#  Developed by: Richard Scott McNew
#
#  Liquid Fortress Widget Processor is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Liquid Fortress Widget Processor is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Liquid Fortress Widget Processor.  If not, see <http://www.gnu.org/licenses/>.

# handle AWS API Gateway requests
import json
import os
import boto3
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pathlib import Path

queue_url = os.environ["QUEUE_URL"]
sqs = boto3.client('sqs')
widget_request_schema = json.load(Path("./widgetRequest-schema.json"))
MAX_RETRY = 3


def validate_json(json_data):
    """Validate the received widget request"""
    try:
        validate(instance=json_data, schema=widget_request_schema)
    except ValidationError as err:
        return False
    return True


def get_json_response(status_code, message):
    """Create a JSON response with the given status code and message"""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {"message": message}
    }


def get_client_error(message):
    """Create a client error message"""
    return get_json_response(400, message)


def get_server_error(message):
    """Create a server error message"""
    return get_json_response(503, message)


def get_success(message):
    """Create a success message"""
    return get_json_response(200, message)


def send_message_or_error(widget_request_str):
    """Put the message on the given SQS queue, retrying if needed;
       Return an error message if there is still failure despite retries;
       Upon successful enqueuing of the message, return the SQS Message ID"""
    retry_count = 0
    while retry_count < MAX_RETRY:
        response = sqs.send_message(QueueUrl=queue_url, MessageBody=widget_request_str)
        if 'MessageId' in response:
            return response['MessageId']
        else:
            retry_count = retry_count + 1
    return None  # Message failed to send despite retry


def lambda_handler(event, context):
    """Handle a widget request event; note that we have request body validation
       enabled on the API Gateway using the widgetRequest JSON schema.  While
       this should catch errors to prevent invocation of this handler, we
       still check for the required widgetRequest fields here too"""
    # Ensure event body exists
    if "body" not in event:
        return get_client_error("Error! No body in request")
    # Get event body
    body = event["body"]
    # Validate widget request JSON against schema
    if not validate_json(body):
        return get_client_error(f"Malformed widget request JSON!  Widget requests must be JSON conforming to the "
                                f"following JSON schema:\n{widget_request_schema}")
    # Send widget request to SQS for processing
    widget_request_str = json.dumps(body)
    message_id = send_message_or_error(widget_request_str)
    if message_id is None:
        return get_server_error(f"SQS Error!  Failed to send widget request: {widget_request_str}")
    return get_success(f"Successfully sent widget request: {widget_request_str}; SQS Message ID: {message_id}")
