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
from botocore.exceptions import ClientError



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
def flatten_widget(worker_id, widget):
    """Flatten widget structure for Dynamo DB use"""
    flat_widget = {}
    for key, value in widget.items():
        if key == OTHER_ATTRIBUTES:
            logging.debug("Widget_Worker_{worker_id}: otherAttributes is: {value}")
            for kv_dict in value:
                logging.debug(f"Widget_Worker_{worker_id}: kv_dict is: {kv_dict}")
                flat_widget[kv_dict[NAME]] = kv_dict[VALUE]
        else:
            flat_widget[key] = value
    return flat_widget


def convert_widget_to_dynamo_db_schema(worker_id, widget):
    """Unpack the widget to match the Dynamo DB table schema"""
    logging.info(f"Widget_Worker_{worker_id}: Converting widget to Dynamo DB schema; input widget is {widget}")
    dynamo_request_widget = {}
    flat_widget = flatten_widget(worker_id, widget)
    for key, value in flat_widget.items():
        dynamo_request_widget[key] = {S: value}
    logging.info(f"Widget_Worker_{worker_id}: Converted Dynamo DB widget is: {dynamo_request_widget}")
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
def update_widget(old_widget, new_widget):
    """Update a JSON-derived widget based on business rules in Homework 2"""
    for key, value in new_widget.items():
        if value == "":
            del old_widget[key]
        elif key == OTHER_ATTRIBUTES:
            for kv_dict in value:
                for oa_key, oa_value in kv_dict.items():
                    if oa_value == "":
                        del old_widget[OTHER_ATTRIBUTES][oa_key]
                    else:
                        old_widget[OTHER_ATTRIBUTES][oa_key] = value[oa_key]
        elif key != WIDGET_ID and key != OWNER:
            old_widget[key] = new_widget[key]
    return old_widget

def update_widget_in_s3(worker_id, s3, output_name, widget):
    """Update the widget in S3 (if it exists)"""
    widget_id = widget[WIDGET_ID]
    widget_owner = widget[OWNER]
    logging.info(f"Widget_Worker_{worker_id}: Updating widget with widget_id {widget_id} in S3 bucket: {output_name}")
    key = f"{WIDGETS}/{widget_owner}/{widget_id}"
    try:
        # get the previously stored widget 
        response = s3.get_object(Bucket=input_name, Key=key)
        old_widget_string = response[BODY].read().decode(UTF8)
        old_widget = json.loads(old_widget_string)
        # update the widget
        updated_widget = update_widget(old_widget, new_widget)
        updated_widget_string = json.dumps(updated_widget)
        # persist the updated widget to S3
        s3.put_object(Bucket=output_name, Key=key, Body=updated_widget_string.encode(UTF8))
    except ClientError as the_client_error:  
        if the_client_error.response[ERROR][CODE] == NO_SUCH_KEY:
            logging.warning(f"Widget_Worker_{worker_id}: Could not find widget_id {widget_id} for owner {widget_owner} for update using S3 key {key}; continuing processing")
        else: 
            raise

# Dynamo DB
def convert_widget_to_dynamo_db_update_expression(worker_id, widget):
    """Convert update widget to update expression"""
    # this API is ugly
    first=True
    update_expression = "SET "
    expression_attribute_names = {}
    expression_attribute_values = {}
    for key, value in widget.items():
        if key != WIDGET_ID and key != OWNER:
            sanitized_key = key.replace("-", "_")
            attribute_name = f"#attr{sanitized_key}"
            symbol = f":new{sanitized_key}"
            if first:
                first = False
                update_expression += f"{attribute_name} = {symbol}"
            else:
                update_expression += f", {attribute_name} = {symbol}"
            expression_attribute_values[symbol] = {S: value}
            expression_attribute_names[attribute_name] = key
    return update_expression, expression_attribute_names, expression_attribute_values

def update_widget_in_dynamo_db(worker_id, dynamodb, output_name, widget):
    """Update the widget in Dynamo DB (if it exists)"""
    widget_id = widget[WIDGET_ID]
    widget_owner = widget[OWNER]
    logging.info(f"Widget_Worker_{worker_id}: Updating widget with widget_id {widget_id} in DYNAMO DB table: {output_name}")
    key = {WIDGET_ID: {S: widget_id}, OWNER: {S: widget_owner}}
    flat_widget = flatten_widget(worker_id, widget)
    (update_expression, expression_attribute_names, expression_attribute_values) = convert_widget_to_dynamo_db_update_expression(worker_id, flat_widget)
    logging.info(f"Widget_Worker_{worker_id}: Updating Dynamo DB widget: key {key}; update_expression {update_expression}; expression_attribute_names {expression_attribute_names}; expression_attribute_values {expression_attribute_values}")
    dynamodb.update_item(TableName=output_name, 
                         Key=key, 
                         UpdateExpression=update_expression, 
                         ExpressionAttributeNames=expression_attribute_names, 
                         ExpressionAttributeValues=expression_attribute_values) 

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
    logging.info(f"Widget_Worker_{worker_id}: Deleting widget with widget_id {widget_id} in S3 bucket: {output_name}")
    key = f"{WIDGETS}/{widget_owner}/{widget_id}"
    s3.delete_object(Bucket=output_name, Key=key)

# Dynamo DB
def delete_widget_from_dynamo_db(worker_id, dynamodb, output_name, widget):
    """Delete the widget from Dynamo DB"""
    widget_id = widget[WIDGET_ID]
    widget_owner = widget[OWNER]
    logging.info(f"Widget_Worker_{worker_id}: Deleting widget with widget_id {widget_id} in DYNAMO DB table: {output_name}")
    key = {WIDGET_ID: {S: widget_id}, OWNER: {S: widget_owner}}
    dynamodb.delete_item(TableName=output_name, Key=key)

# delete widget entry point
def delete_widget(worker_id, s3, dynamodb, args, widget):
    """Delete the widget at the specified output"""
    if args.output_type == S3:
        put_widget_to_s3(worker_id, s3, args.output_name, widget)

    elif args.output_type == DYNAMO_DB:
        delete_widget_from_dynamo_db(worker_id, dynamodb, args.output_name, widget)
