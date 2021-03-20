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

from pathlib import Path
import logging


def init(filename):
    # log to stderr
    console_handler = logging.StreamHandler()

    # also log to specified filename
    log_filename=Path(f"./{filename}.log")
    log_filemode='w'  # overwrite any previous log
    file_handler = logging.FileHandler(log_filename, mode=log_filemode)
    log_handlers = [file_handler, console_handler]

    # default log level
    log_level=logging.INFO

    # log line format
    log_format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d : %(message)s'

    logging.basicConfig(level=log_level, format=log_format, handlers=log_handlers)
    logging.info(f"{filename} starting up")
