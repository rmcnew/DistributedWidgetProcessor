# Functions to handle getting a widget from various input sources
import logging
import os
import random
from pathlib import Path

import boto3

from constants import *


# Local disk
def get_random_filename_or_none_local_disk(input_name):
    logging.info("Checking {} for input widget requests".format(input_name))
    entries = os.listdir(Path(input_name))
    # logging.info("Found {} entries".format(len(entries)))
    files = []
    for entry in entries:
        if os.path.isfile(Path("{}/{}".format(input_name, entry))):
            files.append(entry)
    if len(files) == 0:
        return None
    else:
        return random.choice(files)


def create_local_disk_work_locations(worker_id, input_name):
    """Create work locations in the local disk input directory if they do not already exist.  Work locations are:
    'processing' for widgets currently being processed,
    'completed' for widgets that were previously processed, and
    'error' for widgets that failed to process despite retries"""
    for location in [PROCESSING_LOCATION, COMPLETED_LOCATION, ERROR_LOCATION]:
        logging.info(
            "Widget_Worker_{}: Creating {} work location in {} if not already present".format(worker_id, location,
                                                                                              input_name))
        Path("{}/{}".format(input_name, location)).mkdir(parents=True, exist_ok=True)


def idempotent_rename(worker_id, source, destination):
    try:
        if os.path.exists(source) and not os.path.exists(destination):
            os.rename(source, destination)
    except FileNotFoundError:
        logging.warning(
            "Widget_Worker_{}: Could not move {} to {}; probably done by another worker ".format(worker_id, source,
                                                                                                 destination))


def move_from_input_to_processing_local_disk(worker_id, filename, input_name):
    """Move a widget file from input to processing"""
    input_filename = Path("{}/{}".format(input_name, filename))
    processing_filename = Path("{}/{}/{}".format(input_name, PROCESSING_LOCATION, filename))
    logging.info("Widget_Worker_{}: Moving {} to {}".format(worker_id, input_filename, processing_filename))
    idempotent_rename(worker_id, input_filename, processing_filename)


def move_from_processing_to_completed_local_disk(worker_id, filename, input_name):
    """Move a widget file from processing to completed"""
    processing_filename = Path("{}/{}/{}".format(input_name, PROCESSING_LOCATION, filename))
    completed_filename = Path("{}/{}/{}".format(input_name, COMPLETED_LOCATION, filename))
    logging.info("Widget_Worker_{}: Moving {} to {}".format(worker_id, processing_filename, completed_filename))
    idempotent_rename(worker_id, processing_filename, completed_filename)


def move_from_processing_to_error_local_disk(worker_id, filename, input_name):
    """Move a widget file from processing to error"""
    processing_filename = Path("{}/{}/{}".format(input_name, PROCESSING_LOCATION, filename))
    error_filename = Path("{}/{}/{}".format(input_name, ERROR_LOCATION, filename))
    logging.info("Widget_Worker_{}: Moving {} to {}".format(worker_id, processing_filename, error_filename))
    idempotent_rename(worker_id, processing_filename, error_filename)


def get_widget_from_local_disk(worker_id, input_name):
    """Get a widget from the local disk for processing."""
    filename = get_random_filename_or_none_local_disk(input_name)
    if filename is None:
        return None, ""
    input_filename = Path("{}/{}".format(input_name, filename))
    logging.info("Widget_Worker_{}: Getting widget from {} file at {}".format(worker_id, filename, input_name))
    with open(input_filename, 'r') as file:
        contents = file.read().replace('\n', '')
    return filename, contents


# S3
def rename_s3_object(worker_id, input_name, source, destination):
    """Rename an object within the same bucket"""
    logging.info("Widget_Worker_{}: Moving {} to {} in S3 bucket {}".format(worker_id, source, destination, input_name))
    s3 = boto3.client('s3')
    s3.copy_object(Bucket=input_name, CopySource="{}/{}".format(input_name, source), Key=destination)
    s3.delete_object(Bucket=input_name, Key=source)


def move_from_input_to_processing_s3(worker_id, key, input_name):
    """Move a widget key from input to processing"""
    processing_key = "{}/{}".format(PROCESSING_LOCATION, key)
    logging.info("Widget_Worker_{}: Moving {} to {}".format(worker_id, key, processing_key))
    rename_s3_object(worker_id, input_name, key, processing_key)


def move_from_processing_to_completed_s3(worker_id, key, input_name):
    """Move a widget key from processing to completed"""
    processing_key = "{}/{}".format(PROCESSING_LOCATION, key)
    completed_key = "{}/{}".format(COMPLETED_LOCATION, key)
    logging.info("Widget_Worker_{}: Moving {} to {}".format(worker_id, processing_key, completed_key))
    rename_s3_object(worker_id, input_name, processing_key, completed_key)


def move_from_processing_to_error_s3(worker_id, key, input_name):
    """Move a widget key from processing to error"""
    processing_key = "{}/{}".format(PROCESSING_LOCATION, key)
    error_key = "{}/{}".format(ERROR_LOCATION, key)
    logging.info("Widget_Worker_{}: Moving {} to {}".format(worker_id, processing_key, error_key))
    rename_s3_object(worker_id, input_name, processing_key, error_key)


def get_widget_from_s3_in_key_order(worker_id, input_name):
    """Get the first widget from the specified S3 bucket for processing"""
    # open s3 bucket
    s3 = boto3.client('s3')
    some_objects = s3.list_objects_v2(Bucket=input_name, MaxKeys=S3_MAX_KEYS_TO_LIST, Delimiter="/")
    if CONTENTS not in some_objects:
        return None, ""
    key_to_use = some_objects[CONTENTS][0][KEY]
    logging.info("Widget_Worker_{}: Getting widget for key {}".format(worker_id, key_to_use))
    # read contents
    response = s3.get_object(Bucket=input_name, Key=key_to_use)
    widget_string = response[BODY].read().decode(UTF8)
    return key_to_use, widget_string


def get_widget_from_s3(worker_id, input_name):
    """Get a widget from the specified S3 bucket for processing"""
    # open s3 bucket
    s3 = boto3.client('s3')
    some_objects = s3.list_objects_v2(Bucket=input_name, MaxKeys=S3_MAX_KEYS_TO_LIST, Delimiter="/")
    if CONTENTS not in some_objects:
        return None, ""
    index = random.choice(range(some_objects[KEY_COUNT]))
    key_to_use = some_objects[CONTENTS][index][KEY]
    logging.info("Widget_Worker_{}: Getting widget for key {}".format(worker_id, key_to_use))
    # read contents
    response = s3.get_object(Bucket=input_name, Key=key_to_use)
    widget_string = response[BODY].read().decode(UTF8)
    return key_to_use, widget_string
