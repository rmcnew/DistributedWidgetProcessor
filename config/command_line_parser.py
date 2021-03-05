import argparse
import logging
from shared.constants import *


def parse_command_line():
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
                        type=int)
    args = parser.parse_args()
    return args
