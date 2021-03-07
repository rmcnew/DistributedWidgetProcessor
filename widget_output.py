# Functions to handle widget operations for various output sinks
import logging
import os
from pathlib import Path
from constants import *


# Local disk
def create_local_disk_output_directories(id, output_name, widget_owner):
    """Create widget_owner directory in the local disk output directory if it does not already exist."""
    logging.info(
        "Widget_Worker_{}: Creating {} widget_owner directory in {} if not already present".format(id, widget_owner,
                                                                                                   output_name))
    Path("{}/{}".format(output_name, widget_owner)).mkdir(parents=True, exist_ok=True)




def put_widget_to_local_disk(id, output_name, widget_id, widget_owner, widget):
    """Put the widget to local disk"""
    logging.info(
        "Widget_Worker_{}: Putting widget_id: {} for owner: {} in {}".format(id, widget_id, widget_owner, output_name))
    output_filename = Path("{}/{}/{}".format(output_name, widget_owner, widget_id))
    with open(output_filename, 'w') as file:
        file.write(widget)



def put_widget_to_s3(name):
    None


def put_widget_to_dynamo_db(name):
    None
