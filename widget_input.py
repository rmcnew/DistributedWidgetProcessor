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

# Functions to handle getting a widget from various input sources
import logging

from constants import *


# SQS
def get_widget_requests_from_sqs(worker_id, sqs, args):
    """Get widget requests from the specified SQS queue"""
    logging.info(f"Widget_Worker_{worker_id}: Getting {SQS_MESSAGE_COUNT} message(s) from SQS queue: {args.input_name}")
    messages = {}
    response = sqs.receive_message(QueueUrl=args.input_name, WaitTimeSeconds=SQS_WAIT_TIME, MaxNumberOfMessages=SQS_MESSAGE_COUNT)
    if MESSAGES in response:
        response_messages = response[MESSAGES]  
        for response_message in response_messages:
            if RECEIPT_HANDLE in response_message and BODY in response_message:
                receipt_handle = response_message[RECEIPT_HANDLE]
                messages[receipt_handle] = response_message[BODY]
            else:
                logging.error(f"Widget_Worker_{worker_id}: Receipt_Handle or Body not found in message: {response_message}")
    return messages

def delete_widget_request_from_sqs(worker_id, sqs, args, message_handle):
    """Delete widget request message from SQS"""
    logging.info(f"Widget_Worker_{worker_id}: Deleting SQS message with message_handle {message_handle}")
    sqs.delete_message(QueueUrl=args.input_name, ReceiptHandle=message_handle)

