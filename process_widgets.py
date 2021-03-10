# main entry point for widget processing
import json
import logging
import time
from multiprocessing import Process

import command_line_parser
import widget_processor
import widget_input
import widget_output
from constants import *

workers = []


def process_widgets(worker_id, args):
    logging.info("Widget_Worker_{}: starting up".format(worker_id))
    input_retries_left = args.input_retry_max

    while True:
        (input_key, widget_string) = widget_input.get_widget(worker_id, args)
        if input_key is None:  # no widgets ready
            if input_retries_left > 0:
                logging.info("Widget_Worker_{}: No widgets ready for processing.  Sleeping {} seconds."
                             .format(worker_id, args.input_retry_sleep))
                time.sleep(args.input_retry_sleep)
                input_retries_left = input_retries_left - 1
                logging.info("Widget_Worker_{}: {} retries left".format(worker_id, input_retries_left))
                continue
            else:
                logging.info("Widget_Worker_{}: No retries left.  Exiting.".format(worker_id))
                break
        else:  # parse widget request and process it
            logging.info("Widget_Worker_{}: processing widget: {}".format(worker_id, widget_string))
            widget = json.loads(widget_string)
            # only handle CREATE requests for now, move other requests to completed
            if widget[TYPE] == CREATE:
                # create the widget
                widget_to_store = widget_processor.create_widget(worker_id, widget)
                widget_output.put_widget(worker_id, args, widget_to_store)
            # move the widget to completed or delete if requested
            widget_input.move_to_completed_or_delete(worker_id, args, input_key)


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
        for worker_id in range(args.parallel):
            worker = Process(target=process_widgets, args=(worker_id, args))
            worker.start()
            workers.append(worker)
        logging.info("Workers started.  Waiting for completion")
        for worker in workers:
            worker.join()
    # Process widgets in the main process
    else:
        logging.info("Processing widgets in single process mode")
        process_widgets(0, args)


if __name__ == '__main__':
    main()
