import os


def get_widgets_from_local_disk(name, queue):
    for filename in os.listdir(name):
        # open file and get contents
        with open(filename, 'r') as file:
            contents = file.read().replace('\n', '')
            # place file contents in queue
            queue.put(contents)


def get_widgets_from_s3(name, queue):
    # open s3 bucket
    # read contents
    # place on queue
    None