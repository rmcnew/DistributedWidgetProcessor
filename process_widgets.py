# main entry point for widget processing
import logging
import command_line_parser
import widget_input
from constants import *
from multiprocessing import Process

workers = []

def process_widget(id, args):
    logging.info("Widget_Worker_{}: starting up".format(id))
    # connect to input source
    if args.input_type == LOCAL_DISK:
        logging.info("Using LOCAL DISK input with path: {}".format(args.input_name))
        widget_input.create_local_disk_work_locations(args.input_name)
        widget_string = widget_input.get_widget_from_local_disk(args.input_name, args.dry_run)
        logging.info("Widget_Worker_{}: processing widget: {}".format(id, widget_string))

    elif args.input_type == S3:
        logging.info("Using S3 input with bucket: {}".format(args.input_name))

    # parse widget request


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
                        filename="widget_processing.log",
                        filemode="w",
                        level=logging.INFO)
    # process command line arguments
    args = command_line_parser.parse_command_line()
    # spin up workers to process queue
    if args.parallel and args.parallel > 1:
        logging.info("Starting {} parallel workers to process widgets".format(args.parallel))
        for id in range(args.parallel):
            worker = Process(target=process_widget, args=(id, args))
            worker.start()
            workers.append(worker)
        logging.info("Workers started.  Waiting for completion")
        for worker in workers:
            worker.join()

    else:
        logging.info("Processing widgets in single process mode")
        process_widget(0, args)



if __name__ == '__main__':
    main()
