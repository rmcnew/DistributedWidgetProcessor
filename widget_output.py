# Functions to handle widget operations for various output sinks
import json
import logging
from pathlib import Path

import boto3

from constants import *


# Local disk
def create_local_disk_output_directories(worker_id, output_name, widget_owner):
    """Create widget_owner directory in the local disk output directory if it does not already exist."""
    logging.info(
        "Widget_Worker_{}: Creating {} widget_owner directory in {} if not already present".format(worker_id,
                                                                                                   widget_owner,
                                                                                                   output_name))
    Path("{}/{}".format(output_name, widget_owner)).mkdir(parents=True, exist_ok=True)


def put_widget_to_local_disk(worker_id, output_name, widget_id, widget_owner, widget):
    """Put the widget to local disk"""
    logging.info(
        "Widget_Worker_{}: Putting widget_id: {} for owner: {} in {}".format(worker_id, widget_id, widget_owner,
                                                                             output_name))
    output_filename = Path("{}/{}/{}".format(output_name, widget_owner, widget_id))
    with open(output_filename, 'w') as file:
        file.write(widget)


def put_widget_to_s3(worker_id, output_name, widget_id, widget_owner, widget):
    """Put the widget in the given S3 bucket using the prefix scheme:  widgets/{owner}/{widget_id}"""
    logging.info(
        "Widget_Worker_{}: Putting widget_id: {} for owner: {} in S3 bucket {}".format(worker_id, widget_id,
                                                                                       widget_owner,
                                                                                       output_name))
    output_key = "{}/{}/{}".format(WIDGETS, widget_owner, widget_id)
    s3 = boto3.client('s3')
    s3.put_object(Bucket=output_name, Key=output_key, Body=widget.encode(UTF8))


def convert_widget_to_dynamo_db_schema(worker_id, widget):
    """Unpack the widget to match the Dynamo DB table schema"""
    logging.debug(
        "Widget_Worker_{}: Converting widget to Dynamo DB schema; input widget is {}".format(worker_id, widget))
    dynamo_request_widget = {}
    flat_widget = {}
    for key, value in widget.items():
        if key == OTHER_ATTRIBUTES:
            logging.debug("Widget_Worker_{}: otherAttributes is: {}".format(worker_id, value))
            for kvDict in value:
                logging.debug("Widget_Worker_{}: kvDict is: {}".format(worker_id, kvDict))
                flat_widget[kvDict[NAME]] = kvDict[VALUE]
        else:
            flat_widget[key] = value
    for key, value in flat_widget.items():
        dynamo_request_widget[key] = {S: value}
    logging.debug("Widget_Worker_{}: Converted Dynamo DB widget is: {}".format(worker_id, dynamo_request_widget))
    return dynamo_request_widget


def put_widget_to_dynamo_db(worker_id, output_name, widget_id, widget_owner, widget):
    """Put the widget into the specified Dynamo DB table"""
    logging.info(
        "Widget_Worker_{}: Putting widget_id: {} for owner: {} in Dynamo DB table {}".format(worker_id, widget_id,
                                                                                             widget_owner,
                                                                                             output_name))
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
    if args.output_type == LOCAL_DISK:
        logging.debug("Widget_Worker_{}: Using LOCAL_DISK output with path: {}".format(worker_id, args.output_name))
        create_local_disk_output_directories(worker_id, args.output_name, widget_owner)
        put_widget_to_local_disk(worker_id, args.output_name, widget_id, widget_owner, widget_to_store_string)

    elif args.output_type == S3:
        logging.debug("Widget_Worker_{}: Using S3 output with bucket: {}".format(worker_id, args.output_name))
        put_widget_to_s3(worker_id, args.output_name, widget_id, widget_owner, widget_to_store_string)

    elif args.output_type == DYNAMO_DB:
        logging.debug("Widget_Worker_{}: Using DYNAMO DB output with table: {}".format(worker_id, args.output_name))
        # Note that we pass in the widget_to_store object rather than widget_to_store_string
        put_widget_to_dynamo_db(worker_id, args.output_name, widget_id, widget_owner, widget_to_store)
