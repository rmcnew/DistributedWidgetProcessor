import argparse
from shared.constants import *


def parse_command_line():
    parser = argparse.ArgumentParser(description='Liquid Fortress Widget Processor')
    parser._optionals.title = "Command-line arguments"  # All of the arguments are required
    parser.add_argument("--input-type",
                        help="What type of widget input source should be used?  Valid choices are: S3",
                        action="store",
                        required=True,
                        choices=[S3],
                        default=S3)
    parser.add_argument("--input-name",
                        help="Name or identifier of the widget input source",
                        action="store",
                        required=True)
    parser.add_argument("--output-type",
                        help="What type of widget output sink should be used?  Valid choices are: S3, DynamoDB",
                        action="store",
                        required=True,
                        choices=[S3, DYNAMO_DB],
                        default=S3)
    parser.add_argument("--output-name",
                        help="Name or identifier of the widget output sink",
                        action="store",
                        required=True)
    args = parser.parse_args()
    return args
