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

# functions for update and delete later
