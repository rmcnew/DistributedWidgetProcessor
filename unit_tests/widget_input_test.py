import unittest
import tempfile
import time
import uuid
from pathlib import Path
from constants import *
import widget_input


class WidgetInputTestCases(unittest.TestCase):
    def test_create_local_disk_work_locations(self):
        tmp_dir = tempfile.gettempdir()
        widget_input.create_local_disk_work_locations('X', tmp_dir)
        time.sleep(1)  # wait to ensure directories are created
        expected_paths = [
            Path("{}/{}".format(tmp_dir, PROCESSING_LOCATION)),
            Path("{}/{}".format(tmp_dir, COMPLETED_LOCATION)),
            Path("{}/{}".format(tmp_dir, ERROR_LOCATION))
        ]
        for expected_path in expected_paths:
            self.assertTrue(expected_path.exists())
            expected_path.rmdir()

    def test_move_from_input_to_processing_local_disk(self):
        tmp_filename = uuid.uuid4()
        tmp_dir = tempfile.gettempdir()
        widget_input.create_local_disk_work_locations('X', tmp_dir)
        time.sleep(1)  # wait to ensure directories are created
        processing_path = Path("{}/{}".format(tmp_dir, PROCESSING_LOCATION))
        temp_path = Path("{}/{}".format(tmp_dir, tmp_filename))
        temp_path.touch()
        time.sleep(1)
        self.assertTrue(temp_path.exists())
        widget_input.move_from_input_to_processing_local_disk('X', tmp_filename, tmp_dir)
        tmp_processing_path = Path("{}/{}".format(processing_path, tmp_filename))
        self.assertTrue(tmp_processing_path.exists())
        tmp_processing_path.unlink()
        time.sleep(1)
        expected_paths = [
            Path("{}/{}".format(tmp_dir, PROCESSING_LOCATION)),
            Path("{}/{}".format(tmp_dir, COMPLETED_LOCATION)),
            Path("{}/{}".format(tmp_dir, ERROR_LOCATION))
        ]
        for expected_path in expected_paths:
            self.assertTrue(expected_path.exists())
            expected_path.rmdir()

    def test_move_from_processing_to_completed_local_disk(self):
        tmp_filename = uuid.uuid4()
        tmp_dir = tempfile.gettempdir()
        widget_input.create_local_disk_work_locations('X', tmp_dir)
        time.sleep(1)  # wait to ensure directories are created
        processing_path = Path("{}/{}".format(tmp_dir, PROCESSING_LOCATION))
        completed_path = Path("{}/{}".format(tmp_dir, COMPLETED_LOCATION))
        tmp_processing_path = Path("{}/{}".format(processing_path, tmp_filename))
        tmp_processing_path.touch()
        time.sleep(1)
        self.assertTrue(tmp_processing_path.exists())
        widget_input.move_from_processing_to_completed_local_disk('X', tmp_filename, tmp_dir)
        tmp_completed_path = Path("{}/{}".format(completed_path, tmp_filename))
        self.assertTrue(tmp_completed_path.exists())
        tmp_completed_path.unlink()
        time.sleep(1)
        expected_paths = [
            Path("{}/{}".format(tmp_dir, PROCESSING_LOCATION)),
            Path("{}/{}".format(tmp_dir, COMPLETED_LOCATION)),
            Path("{}/{}".format(tmp_dir, ERROR_LOCATION))
        ]
        for expected_path in expected_paths:
            self.assertTrue(expected_path.exists())
            expected_path.rmdir()

    def test_move_from_processing_to_error_local_disk(self):
        tmp_filename = uuid.uuid4()
        tmp_dir = tempfile.gettempdir()
        widget_input.create_local_disk_work_locations('X', tmp_dir)
        time.sleep(1)  # wait to ensure directories are created
        processing_path = Path("{}/{}".format(tmp_dir, PROCESSING_LOCATION))
        error_path = Path("{}/{}".format(tmp_dir, ERROR_LOCATION))
        tmp_processing_path = Path("{}/{}".format(processing_path, tmp_filename))
        tmp_processing_path.touch()
        time.sleep(1)
        self.assertTrue(tmp_processing_path.exists())
        widget_input.move_from_processing_to_error_local_disk('X', tmp_filename, tmp_dir)
        tmp_error_path = Path("{}/{}".format(error_path, tmp_filename))
        self.assertTrue(tmp_error_path.exists())
        tmp_error_path.unlink()
        time.sleep(1)
        expected_paths = [
            Path("{}/{}".format(tmp_dir, PROCESSING_LOCATION)),
            Path("{}/{}".format(tmp_dir, COMPLETED_LOCATION)),
            Path("{}/{}".format(tmp_dir, ERROR_LOCATION))
        ]
        for expected_path in expected_paths:
            self.assertTrue(expected_path.exists())
            expected_path.rmdir()


if __name__ == '__main__':
    unittest.main()
