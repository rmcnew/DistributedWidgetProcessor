import logging
from config import command_line_parser
from shared.constants import *

processes = []


def process_widget_worker(args):
    # connect to input source
    if args.input_type == LOCAL_DISK:
        logging.info("Using LOCAL DISK input with path: {}".format(args.input_name))

    elif args.input_type == S3:
        logging.info("Using S3 input with bucket: {}".format(args.input_name))

    # connect to output sink
    if args.output_type == LOCAL_DISK:
        logging.info("Using LOCAL_DISK output with path: {}".format(args.output_name))

    elif args.output_type == S3:
        logging.info("Using S3 output with bucket: {}".format(args.output_name))

    elif args.output_type == DYNAMO_DB:
        logging.info("Using DYNAMO DB output with table: {}".format(args.output_name))


def main():
    # initialize logging
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d : %(message)s',
                        filename="process_widgets.log",
                        level=logging.INFO)
    # process command line arguments
    args = command_line_parser.parse_command_line()
    process_widget_worker(args)


if __name__ == '__main__':
    main()
