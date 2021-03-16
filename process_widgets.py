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

# main entry point for widget processing
import logging
from multiprocessing import Process

import logger
from command_line_parser import parse_command_line
from widget_processor import process_widgets
from enqueue_worker import s3_bucket_to_sqs
from constants import *
from widget_input import create_temporary_queue, delete_temporary_queue

workers = []


def main():
    temp_queue = ""
    # initialize logging
    logger.init("Process_Widgets")
    # process command line arguments
    args = parse_command_line()
    # spin up an enqueue worker if S3 is used as the input source
    if args.input_type == S3:
        temp_queue = create_temporary_queue()
        nq_worker = Process(
            target=s3_bucket_to_sqs,
            args=(args.input_name, temp_queue, args.input_retry_max, args.input_retry_sleep)
        )
        nq_worker.start()
        workers.append(nq_worker)
        args.input_name = temp_queue
    # spin up worker processes to do parallel widget processing
    if args.parallel and args.parallel > 1:
        logging.info(f"Starting {args.parallel} parallel workers to process widgets")
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
    if args.input_type == S3:
        delete_temporary_queue(temp_queue)


if __name__ == '__main__':
    main()
