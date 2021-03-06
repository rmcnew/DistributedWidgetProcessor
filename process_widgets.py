# main entry point for widget processing
import json
import logging
from multiprocessing import Process

import command_line_parser
import widget_input
import widget_output
from constants import *

workers = []


def process_widget(id, args):
    logging.info("Widget_Worker_{}: starting up".format(id))
    filename = None
    widget_string = ""

    while True:
        # connect to input source
        if args.input_type == LOCAL_DISK:
            logging.info("Widget_Worker_{}: Using LOCAL DISK input with path: {}".format(id, args.input_name))
            widget_input.create_local_disk_work_locations(id, args.input_name)
            (filename, widget_string) = widget_input.get_widget_from_local_disk(id, args.input_name)
            if filename is None:
                break
            widget_input.move_from_input_to_processing_local_disk(id, filename, args.input_name)
            logging.info("Widget_Worker_{}: processing widget: {}".format(id, widget_string))

        elif args.input_type == S3:
            logging.info("Widget_Worker_{}: Using S3 input with bucket: {}".format(id, args.input_name))

        # parse widget request
        widget = json.loads(widget_string)
        if widget[TYPE] != CREATE:
            # only handle CREATE requests for now, move other requests to completed
            widget_input.move_from_processing_to_completed_local_disk(id, filename, args.input_name)
            continue
        widget_id = widget[WIDGET_ID]
        widget_owner = widget[OWNER].replace(" ", "-")
        logging.info("Widget_Worker_{}: Found widget_id: {} and owner: {}".format(id, widget_id, widget_owner))
        widget_to_store = {WIDGET_ID: widget_id,
                           OWNER: widget_owner,
                           LABEL: widget[LABEL],
                           DESCRIPTION: widget[DESCRIPTION],
                           OTHER_ATTRIBUTES: widget[OTHER_ATTRIBUTES]}
        widget_to_store_string = json.dumps(widget_to_store)

        # connect to output sink
        if args.output_type == LOCAL_DISK:
            logging.info("Widget_Worker_{}: Using LOCAL_DISK output with path: {}".format(id, args.output_name))
            widget_output.create_local_disk_output_directories(id, args.output_name, widget_owner)
            widget_output.put_widget_to_local_disk(id, args.output_name, widget_id, widget_owner, widget_to_store_string)
            widget_input.move_from_processing_to_completed_local_disk(id, filename, args.input_name)

        elif args.output_type == S3:
            logging.info("Widget_Worker_{}: Using S3 output with bucket: {}".format(id, args.output_name))

        elif args.output_type == DYNAMO_DB:
            logging.info("Widget_Worker_{}: Using DYNAMO DB output with table: {}".format(id, args.output_name))


def main():
    # initialize logging
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d : %(message)s',
                        filename="Process_Widgets.log",
                        filemode="w",
                        level=logging.INFO)
    # process command line arguments
    args = command_line_parser.parse_command_line()
    # spin up worker processes to do parallel widget processing
    if args.parallel and args.parallel > 1:
        logging.info("Starting {} parallel workers to process widgets".format(args.parallel))
        for id in range(args.parallel):
            worker = Process(target=process_widget, args=(id, args))
            worker.start()
            workers.append(worker)
        logging.info("Workers started.  Waiting for completion")
        for worker in workers:
            worker.join()
    # Process widgets in the main process
    else:
        logging.info("Processing widgets in single process mode")
        process_widget(0, args)


if __name__ == '__main__':
    main()
