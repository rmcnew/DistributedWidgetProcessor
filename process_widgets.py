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

import command_line_parser
from widget_processor import process_widgets

workers = []


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
