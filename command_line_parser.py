# Parse and validate command line arguments
import argparse
import logging
import os
import sys
from constants import *


def parse_command_line(maybe_args=None):
    logging.info("Processing command line arguments")
    parser = argparse.ArgumentParser(description='Liquid Fortress Widget Processor')
    parser._optionals.title = "Command-line arguments"  # All of the arguments are required
    parser.add_argument("--input-type",
                        help="What type of widget input source should be used?  Valid choices are: LOCAL_DISK, S3",
                        action="store",
                        required=True,
                        choices=[LOCAL_DISK, S3],
                        default=LOCAL_DISK)
    parser.add_argument("--input-name",
                        help="Name, path, or identifier of the widget input source",
                        action="store",
                        required=True)
    parser.add_argument("--output-type",
                        help="What type of widget output sink should be used?  Valid choices are: LOCAL_DISK, S3, "
                             "DynamoDB",
                        action="store",
                        required=True,
                        choices=[LOCAL_DISK, S3, DYNAMO_DB],
                        default=LOCAL_DISK)
    parser.add_argument("--output-name",
                        help="Name, path, or identifier of the widget output sink",
                        action="store",
                        required=True)
    parser.add_argument("--parallel",
                        help="How many parallel workers to run for widget processing?",
                        action="store",
                        required=False,
                        default=1,
                        type=int)
    parser.add_argument("--delete-completed",
                        help="Delete widget requests after they are completed",
                        action="store_true",
                        required=False,
                        default=False)
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
