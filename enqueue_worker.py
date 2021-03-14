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

# functions to handle getting widget requests from S3 and enqueuing in SQS
import logging
import time

import boto3
from botocore.exceptions import ClientError

import logger
from constants import *
from command_line_parser import enqueue_worker_parse_command_line


def enqueue_object_list(s3, sqs, args, object_list):
    """Extract object list from S3, enqueue in SQS, delete from S3"""
    for object_info in object_list:
        # get s3 key and widget request
        key = object_info[KEY]
        logging.info(f"Enqueue_Worker: Getting widget for key {key}")
        response = s3.get_object(Bucket=args.bucket, Key=key)
        widget_request = response[BODY].read().decode(UTF8)
        # enqueue widget request
        logging.info(f"Enqueue_Worker: enqueuing widget request: {widget_request}")
        sqs.send_message(QueueUrl=args.queue, MessageBody=widget_request)
        # delete widget in s3
        logging.info(f"Enqueue_Worker: Deleting enqueued widget from S3: {key}")
        s3.delete_object(Bucket=args.bucket, Key=key)


def main():
    """Entry point for Enqueue Worker"""
    # initialize logging
    logger.init("Enqueue_Worker")
    # process command line arguments to get S3 bucket name and SQS queue URL
    args = enqueue_worker_parse_command_line()
    # create AWS clients
    s3 = boto3.client('s3')
    sqs = boto3.client('sqs')

    retries_left = args.input_retry_max

    while True:
        maybe_objects = s3.list_objects_v2(Bucket=args.bucket, MaxKeys=S3_MAX_KEYS_TO_LIST, Delimiter="/")
        if CONTENTS in maybe_objects:
            enqueue_object_list(s3, sqs, args, maybe_objects[CONTENTS])
        
        # no widgets ready
        elif retries_left > 0:
            logging.info(f"Enqueue_Worker: No widgets ready for processing.  Sleeping {args.input_retry_sleep} seconds.")
            time.sleep(args.input_retry_sleep)
            retries_left = retries_left - 1
            logging.info(f"Enqueue_Worker: {retries_left} retries left")
            continue
        else:
            logging.info(f"Enqueue_Worker: No widget requests found and no retries left.  Exiting.")
            break


if __name__ == '__main__':
    main()
