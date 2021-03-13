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

# Functions to handle widget operations for various output sinks
import json
import logging
from pathlib import Path

import boto3

from constants import *


# S3
def put_widget_to_s3(worker_id, output_name, widget_id, widget_owner, widget):
    """Put the widget in the given S3 bucket using the prefix scheme:  widgets/{owner}/{widget_id}"""
    logging.info(f"Widget_Worker_{worker_id}: Putting widget_id: {widget_id} for owner: {widget_owner} in S3 bucket {output_name}")
    output_key = f"{WIDGETS}/{widget_owner}/{widget_id}"
    s3 = boto3.client('s3')
    s3.put_object(Bucket=output_name, Key=output_key, Body=widget.encode(UTF8))


# Dynamo DB
def convert_widget_to_dynamo_db_schema(worker_id, widget):
    """Unpack the widget to match the Dynamo DB table schema"""
    logging.info(f"Widget_Worker_{worker_id}: Converting widget to Dynamo DB schema; input widget is {widget}")
    dynamo_request_widget = {}
    flat_widget = {}
    for key, value in widget.items():
        if key == OTHER_ATTRIBUTES:
            logging.info("Widget_Worker_{worker_id}: otherAttributes is: {value}")
            for kv_dict in value:
                logging.info(f"Widget_Worker_{worker_id}: kv_dict is: {kv_dict}")
                flat_widget[kv_dict[NAME]] = kv_dict[VALUE]
        else:
            flat_widget[key] = value
    for key, value in flat_widget.items():
        dynamo_request_widget[key] = {S: value}
    logging.info(f"Widget_Worker_{worker_id}: Converted Dynamo DB widget is: {dynamo_request_widget}")
    return dynamo_request_widget


def put_widget_to_dynamo_db(worker_id, output_name, widget_id, widget_owner, widget):
    """Put the widget into the specified Dynamo DB table"""
    logging.info(f"Widget_Worker_{worker_id}: Putting widget_id: {widget_id} for owner: {widget_owner} in Dynamo DB table {output_name}")
    dynamodb = boto3.client('dynamodb')
    dynamodb_widget = convert_widget_to_dynamo_db_schema(worker_id, widget)
    dynamodb.put_item(TableName=output_name, Item=dynamodb_widget)


# main widget_output functions #
def put_widget(worker_id, args, widget_to_store):
    """Put the widget at the specified output"""
    widget_id = widget_to_store[WIDGET_ID]
    widget_owner = widget_to_store[OWNER]
    widget_to_store_string = json.dumps(widget_to_store)
    # connect to output sink
    if args.output_type == S3:
        logging.info(f"Widget_Worker_{worker_id}: Using S3 output with bucket: {args.output_name}")
        put_widget_to_s3(worker_id, args.output_name, widget_id, widget_owner, widget_to_store_string)

    elif args.output_type == DYNAMO_DB:
        logging.info(f"Widget_Worker_{worker_id}: Using DYNAMO DB output with table: {args.output_name}")
        # Note that we pass in the widget_to_store object rather than widget_to_store_string
        put_widget_to_dynamo_db(worker_id, args.output_name, widget_id, widget_owner, widget_to_store)
