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

# Parse and validate command line arguments
import argparse
import logging
import os
import sys
from constants import *


def parse_command_line(maybe_args=None):
    """Parse command line arguments for process_widgets main entry point"""
    logging.info("Processing process_widgets command line arguments")
    parser = argparse.ArgumentParser(description='Liquid Fortress Widget Processor')
    parser._optionals.title = "Command-line arguments"  # All of the arguments are required; overwrite the default title
    parser.add_argument("--input-type",
                        help="What type of widget input source should be used?  Valid choices are: S3, SQS",
                        action="store",
                        required=True,
                        choices=[S3, SQS])
    parser.add_argument("--input-name",
                        help="Bucket name or SQS queue URL for the widget input source",
                        action="store",
                        required=True)
    parser.add_argument("--output-type",
                        help="What type of widget output sink should be used?  Valid choices are: S3, DYNAMO_DB",
                        action="store",
                        required=True,
                        choices=[S3, DYNAMO_DB])
    parser.add_argument("--output-name",
                        help="Bucket name, or Dynamo DB table name for the widget output sink",
                        action="store",
                        required=True)
    parser.add_argument("--parallel",
                        help="How many parallel workers to run for widget processing?",
                        action="store",
                        required=False,
                        default=1,
                        type=int)
    parser.add_argument("--input-retry-max",
                        help="Max number of input poll retries before quitting. Must be positive or 0.",
                        action="store",
                        required=False,
                        default=3,
                        type=int)
    parser.add_argument("--input-retry-sleep",
                        help="How much time in seconds to wait before retrying input poll?  Must be positive or 0.",
                        action="store",
                        required=False,
                        default=2,
                        type=int)
    if maybe_args is not None:
        args = parser.parse_args(maybe_args)
    else:
        args = parser.parse_args()
    if args.input_retry_max < 0:
        print("Illegal Parameter Value:  input-retry-max parameter cannot be negative!")
        parser.print_help()
        sys.exit(os.EX_USAGE)
    if args.input_retry_sleep < 0:
        print("Illegal Parameter Value:  input-retry-sleep parameter cannot be negative!")
        parser.print_help()
        sys.exit(os.EX_USAGE)
    return args

