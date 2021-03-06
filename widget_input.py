# Functions to handle getting a widget from various input sources
from constants import *
import os
import random
import logging
from pathlib import Path


# Local disk
def create_local_disk_work_locations(input_name):
    """Create work locations in the local disk input directory if they do not already exist.  Work locations are:
    'processing' for widgets currently being processed,
    'completed' for widgets that were previously processed, and
    'error' for widgets that failed to process despite retries"""
    for location in [PROCESSING_LOCATION, COMPLETED_LOCATION, ERROR_LOCATION]:
        logging.info("Creating {} work location in {} if not already present".format(location, input_name))
        Path("{}/{}".format(input_name, location)).mkdir(parents=True, exist_ok=True)


def get_widget_from_local_disk(input_name, dry_run=False):
    """Get a widget from the local disk for processing.  Put the widget input file into the 'processing' location"""
    filename = random.choice(os.listdir(input_name))
    input_filename = Path("{}/{}".format(input_name, filename))
    logging.info("Getting widget from {} file at {}".format(filename, input_name))
    with open(input_filename, 'r') as file:
        contents = file.read().replace('\n', '')
    if not dry_run:
        processing_filename = Path("{}/{}/{}".format(input_name, PROCESSING_LOCATION, filename))
        os.rename(input_filename, processing_filename)
    return contents



# S3
def get_widgets_from_s3(input_name):
    # open s3 bucket
    # read contents
    None
