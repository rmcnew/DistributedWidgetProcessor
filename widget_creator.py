# functions to handle creation of a new widget
import logging
from constants import *


def create_widget(worker_id, widget):
    """Create a widget from a widget create request"""
    widget_id = widget[WIDGETID]
    widget_owner = widget[OWNER].replace(" ", "-")
    logging.debug("Widget_Worker_{}: Found widget_id: {} and owner: {}".format(worker_id, widget_id, widget_owner))
    widget_to_store = {WIDGET_ID: widget_id,
                       OWNER: widget_owner,
                       LABEL: widget[LABEL],
                       DESCRIPTION: widget[DESCRIPTION],
                       OTHER_ATTRIBUTES: widget[OTHER_ATTRIBUTES]}
    return widget_to_store
