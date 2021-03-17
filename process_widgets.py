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

from command_line_parser import parse_command_line
from enqueue_worker import s3_bucket_to_sqs
from logger import init
from widget_input import create_temporary_queue, delete_temporary_queue
from widget_processor import process_widgets
from constants import S3

# globals, but only used by functions within this file
workers = []
temp_queue = None


def start_enqueue_worker(args):
    """Create a child process to transfer widget requests from S3 to SQS"""
    logging.info("Creating temporary queue and enqueue worker")
    global temp_queue
    temp_queue = create_temporary_queue()
    nq_worker = Process(
        target=s3_bucket_to_sqs,
        args=(args.input_name, temp_queue, args.input_retry_max, args.input_retry_sleep)
    )
    nq_worker.start()
    workers.append(nq_worker)


def start_widget_workers(args):
    """Create child processes to parallelize widget processing"""
    logging.info(f"Starting {args.parallel} parallel workers to process widgets")
    for worker_id in range(args.parallel):
        worker = Process(target=process_widgets, args=(worker_id, args))
        worker.start()
        workers.append(worker)


def wait_for_workers_to_finish():
    logging.info("Workers started.  Waiting for completion")
    for worker in workers:
        worker.join()
    # clean up temp queue if needed
    if temp_queue is not None:
        delete_temporary_queue(temp_queue)


def main():
    """Main entry point for Liquid Fortress Widget Processor"""
    # initialize logging
    init("Process_Widgets")
    # process command line arguments
    args = parse_command_line()
    # spin up an enqueue worker if S3 is used as the input source
    if args.input_type == S3:
        start_enqueue_worker(args)
        args.input_name = temp_queue
    # if parallel, spin up worker processes to do parallel widget processing
    if args.parallel and args.parallel > 1:
        start_widget_workers(args)
    else:  # otherwise, process widgets in the main process
        logging.info("Processing widgets in single process mode")
        process_widgets(0, args)
    # wait for child processes to finish
    wait_for_workers_to_finish()


if __name__ == '__main__':
    main()
