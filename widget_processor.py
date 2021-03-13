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

import widget_input
import widget_output
from constants import *
from constants import TYPE, CREATE


def create_widget(worker_id, widget):
    """Create a widget from a widget create request"""
    widget_id = widget[WIDGETID]
    widget_owner = widget[OWNER].replace(" ", "-")
    logging.info("Widget_Worker_{worker_id}: Found widget_id: {widget_id} and owner: {widget_owner}")
    widget_to_store = {WIDGET_ID: widget_id,
                       OWNER: widget_owner,
                       LABEL: widget[LABEL],
                       DESCRIPTION: widget[DESCRIPTION],
                       OTHER_ATTRIBUTES: widget[OTHER_ATTRIBUTES]}
    return widget_to_store


def update_widget(worker_id, widget):
    """Update a widget based on widget update request"""


def delete_widget(worker_id, widget):
    """Delete a widget based on widget delete request"""


# functions for update and delete later
def process_widgets(worker_id, args):
    logging.info(f"Widget_Worker_{worker_id}: starting up")
    input_retries_left = args.input_retry_max

    while True:
        (input_key, widget_string) = widget_input.get_widget(worker_id, args)
        if input_key is None:  # no widgets ready
            if input_retries_left > 0:
                logging.info(f"Widget_Worker_{worker_id}: No widgets ready for processing.  Sleeping {args.input_retry_sleep} seconds.")
                time.sleep(args.input_retry_sleep)
                input_retries_left = input_retries_left - 1
                logging.info(f"Widget_Worker_{worker_id}: {input_retries_left} retries left")
                continue
            else:
                logging.info(f"Widget_Worker_{worker_id}: No retries left.  Exiting.")
                break
        else:  # parse widget request and process it
            logging.info(f"Widget_Worker_{worker_id}: processing widget: {widget_string}")
            widget = json.loads(widget_string)
            # only handle CREATE requests for now, move other requests to completed
            if widget[TYPE] == CREATE:
                # create the widget
                widget_to_store = create_widget(worker_id, widget)
                widget_output.put_widget(worker_id, args, widget_to_store)
            # move the widget to completed or delete if requested
            widget_input.move_to_completed_or_delete(worker_id, args, input_key)
