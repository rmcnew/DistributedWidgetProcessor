""" Shared utility functions """
import datetime
import signal
import socket
import subprocess
import tempfile
import sys
import os


def get_ip_address():
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        temp_socket.connect(('192.0.0.8', 1027))
    except socket.error:
        return None
    return temp_socket.getsockname()[0]


def timestamp():
    return datetime.datetime.now().isoformat()


def get_elapsed_time(start_time):
    current_time = datetime.datetime.now()
    elapsed_time = current_time - start_time
    return elapsed_time


def get_temp_dir():
    return tempfile.mkdtemp()


def get_python_interpreter():
    return sys.executable


def get_script_folder():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def run_as_subprocess(command_line):
    split_command_line = command_line.split(' ')
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    completed = subprocess.run(split_command_line, stdin=None)
    return completed
