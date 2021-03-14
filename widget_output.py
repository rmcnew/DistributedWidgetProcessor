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

from constants import *


# ************************* See if widget exists ************************* 
# S3
def widget_exists_in_s3(worker_id, s3, output_name, widget):
    """See if the widget exists in S3"""
    widget_id = widget[WIDGET_ID]
    widget_owner = widget[OWNER]
    logging.info(f"Widget_Worker_{worker_id}: Check existence of widget_id: {widget_id} for owner: {widget_owner} in S3 bucket {output_name}")

# Dynamo DB
def widget_exists_in_dynamo_db(worker_id, dynamodb, output_name, widget):
    """See if the widget exists in Dynamo DB"""
    widget_id = widget[WIDGET_ID]
    widget_owner = widget[OWNER]
    logging.info(f"Widget_Worker_{worker_id}: Check existence of widget_id: {widget_id} for owner: {widget_owner} in Dynamo DB table {output_name}")

# ************************* Create widgets ************************* 
# S3
def put_widget_to_s3(worker_id, s3, output_name, widget):
    """Put the widget in the given S3 bucket using the prefix scheme:  widgets/{owner}/{widget_id}"""
    widget_id = widget[WIDGET_ID]
    widget_owner = widget[OWNER]
    logging.info(f"Widget_Worker_{worker_id}: Putting widget_id: {widget_id} for owner: {widget_owner} in S3 bucket {output_name}")
    widget_to_store_string = json.dumps(widget_to_store)
    output_key = f"{WIDGETS}/{widget_owner}/{widget_id}"
    s3.put_object(Bucket=output_name, Key=output_key, Body=widget_to_store_string.encode(UTF8))


# Dynamo DB
def convert_widget_to_dynamo_db_schema(worker_id, widget):
    """Unpack the widget to match the Dynamo DB table schema"""
    logging.info(f"Widget_Worker_{worker_id}: Converting widget to Dynamo DB schema; input widget is {widget}")
    dynamo_request_widget = {}
    flat_widget = {}
    for key, value in widget.items():
        if key == OTHER_ATTRIBUTES:
            logging.debug("Widget_Worker_{worker_id}: otherAttributes is: {value}")
            for kv_dict in value:
                logging.debug(f"Widget_Worker_{worker_id}: kv_dict is: {kv_dict}")
                flat_widget[kv_dict[NAME]] = kv_dict[VALUE]
        else:
            flat_widget[key] = value
    for key, value in flat_widget.items():
        dynamo_request_widget[key] = {S: value}
    logging.debug(f"Widget_Worker_{worker_id}: Converted Dynamo DB widget is: {dynamo_request_widget}")
    return dynamo_request_widget


def put_widget_to_dynamo_db(worker_id, dynamodb, output_name, widget):
    """Put the widget into the specified Dynamo DB table"""
    widget_id = widget[WIDGET_ID]
    widget_owner = widget[OWNER]
    logging.info(f"Widget_Worker_{worker_id}: Putting widget_id: {widget_id} for owner: {widget_owner} in Dynamo DB table {output_name}")
    dynamodb_widget = convert_widget_to_dynamo_db_schema(worker_id, widget)
    dynamodb.put_item(TableName=output_name, Item=dynamodb_widget)

# create widget entry point
def put_widget(worker_id, s3, dynamodb, args, widget):
    """Put the widget at the specified output"""
    if args.output_type == S3:
        put_widget_to_s3(worker_id, s3, args.output_name, widget)

    elif args.output_type == DYNAMO_DB:
        put_widget_to_dynamo_db(worker_id, dynamodb, args.output_name, widget)



# ************************* Update widgets ************************* 
# S3
def update_widget_in_s3(worker_id, s3, output_name, widget):
    """Update the widget in S3 (if it exists)"""
    widget_id = widget[WIDGET_ID]
    widget_owner = widget[OWNER]
    widget_string = json.dumps(widget)
    logging.info(f"Widget_Worker_{worker_id}: Updating widget with widget_id {widget_id} in S3 bucket: {args.output_name}")

# Dynamo DB
def update_widget_in_dynamo_db(worker_id, dynamodb, output_name, widget):
    """Update the widget in Dynamo DB (if it exists)"""
    widget_id = widget[WIDGET_ID]
    widget_owner = widget[OWNER]
    logging.info(f"Widget_Worker_{worker_id}: Updating widget with widget_id {widget_id} in DYNAMO DB table: {args.output_name}")

# update widget entry point
def update_widget(worker_id, s3, dynamodb, args, widget):
    """Update the widget at the specified output"""
    if args.output_type == S3:
        update_widget_in_s3(worker_id, s3, args.output_name, widget_id, widget_owner, widget_string)

    elif args.output_type == DYNAMO_DB:
        update_widget_in_dynamo_db(worker_id, dynamodb, args.output_name, widget)


# ************************* Delete widgets ************************* 
# S3
def delete_widget_from_s3(worker_id, s3, output_name, widget):
    """Delete the widget from S3"""
    widget_id = widget[WIDGET_ID]
    widget_owner = widget[OWNER]
    logging.info(f"Widget_Worker_{worker_id}: Deleting widget with widget_id {widget_id} in S3 bucket: {args.output_name}")
    key = f"{WIDGETS}/{widget_owner}/{widget_id}"
    s3.delete_object(Bucket=output_name, Key=key)

# Dynamo DB
def delete_widget_from_dynamo_db(worker_id, dynamodb, output_name, widget):
    """Delete the widget from Dynamo DB"""
    widget_id = widget[WIDGET_ID]
    widget_owner = widget[OWNER]
    logging.info(f"Widget_Worker_{worker_id}: Deleting widget with widget_id {widget_id} in DYNAMO DB table: {args.output_name}")
    key = {WIDGET_ID: {S: widget_id}, OWNER: {S: widget_owner}}
    dynamodb.delete_item(TableName=output_name, Key=key)

# delete widget entry point
def delete_widget(worker_id, s3, dynamodb, args, widget):
    """Delete the widget at the specified output"""
    if args.output_type == S3:
        put_widget_to_s3(worker_id, s3, args.output_name, widget)

    elif args.output_type == DYNAMO_DB:
        delete_widget_from_dynamo_db(worker_id, dynamodb, args.output_name, widget)
