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

# functions to handle creation of a new widget
import json
import logging
import time

import boto3
import widget_input
import widget_output
from constants import *

def normalize_widget(worker_id, widget):
    """Replace spaces with dashes in owner; 
       'widgetId' => 'widget_id' to match Dynamo DB table;
       remove type and requestId fields for widget data"""
    normalized_widget = {}
    for key, value in widget.items():
        if key == OWNER:
            normalized_widget[OWNER] = widget[OWNER].replace(" ", "-")
        elif key == WIDGETID:
            normalized_widget[WIDGET_ID] = widget[WIDGETID]
        elif key == TYPE or key == REQUEST_ID:
            continue
        else:
            normalized_widget[key] = value
    return normalized_widget


# functions for update and delete later
def process_widgets(worker_id, args):
    logging.info(f"Widget_Worker_{worker_id}: starting up")
    # create AWS clients
    sqs = boto3.client('sqs')
    s3 = boto3.client('s3')
    dynamodb = boto3.client('dynamodb')

    input_retries_left = args.input_retry_max

    while True:
        # get widget requests from SQS
        widget_requests = widget_input.get_widget_requests_from_sqs(worker_id, sqs, args)
        if len(widget_requests) > 0:  
            for message_handle, widget_request_str in widget_requests.items():
                logging.info(f"Widget_Worker_{worker_id}: processing widget: {widget_request_str}  with message_handle: {message_handle}")
                # parse widget request and process it
                widget = json.loads(widget_request_str)
                # only handle CREATE requests for now, move other requests to completed
                if widget[TYPE] == CREATE:
                    # create the widget
                    widget_to_store = normalize_widget(worker_id, widget)
                    widget_output.put_widget(worker_id, s3, dynamodb, args, widget_to_store)
                elif widget[TYPE] == UPDATE:
                    # update the widget
                    widget_to_update = normalize_widget(worker_id, widget)
                    widget_output.update_widget(worker_id, s3, dynamodb, args, widget_to_update)
                elif widget[TYPE] == DELETE:
                    # delete the widget
                    widget_to_delete = normalize_widget(worker_id, widget)
                    if WIDGET_ID in widget_to_delete and OWNER in widget_to_delete: 
                        widget_output.delete_widget(worker_id, s3, dynamodb, args, widget_to_delete)
                # delete the widget request
                widget_input.delete_widget_request_from_sqs(worker_id, sqs, args, message_handle)
        else: # no widgets to process right now
            if input_retries_left > 0:
                logging.info(f"Widget_Worker_{worker_id}: No widgets ready for processing.  Sleeping {args.input_retry_sleep} seconds.")
                time.sleep(args.input_retry_sleep)
                input_retries_left = input_retries_left - 1
                logging.info(f"Widget_Worker_{worker_id}: {input_retries_left} retries left")
                continue
            else:
                logging.info(f"Widget_Worker_{worker_id}: No widget requests to process and no retries left.  Exiting.")
                break
