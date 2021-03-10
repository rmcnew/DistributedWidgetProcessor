import unittest
import command_line_parser
from io import StringIO
from unittest.mock import patch


class CommandLineParserTestCases(unittest.TestCase):

    @patch('sys.stderr', new_callable=StringIO)
    def test_input_type_required(self, mock_stderr):
        test_args = [
            '--input-name', 'source_bucket',
            '--output-type', 'S3',
            '--output-name', 'sink_bucket']
        with self.assertRaises(SystemExit):
            command_line_parser.parse_command_line(test_args)
        self.assertRegexpMatches(
            mock_stderr.getvalue(),
            r"the following arguments are required: --input-type")

    @patch('sys.stderr', new_callable=StringIO)
    def test_input_name_required(self, mock_stderr):
        test_args = [
            '--input-type', 'S3',
            '--output-type', 'S3',
            '--output-name', 'sink_bucket']
        with self.assertRaises(SystemExit):
            command_line_parser.parse_command_line(test_args)
        self.assertRegexpMatches(
            mock_stderr.getvalue(),
            r"the following arguments are required: --input-name")

    @patch('sys.stderr', new_callable=StringIO)
    def test_output_type_required(self, mock_stderr):
        test_args = [
            '--input-type', 'S3',
            '--input-name', 'source_bucket',
            '--output-name', 'sink_bucket']
        with self.assertRaises(SystemExit):
            command_line_parser.parse_command_line(test_args)
        self.assertRegexpMatches(
            mock_stderr.getvalue(),
            r"the following arguments are required: --output-type")

    @patch('sys.stderr', new_callable=StringIO)
    def test_output_name_required(self, mock_stderr):
        test_args = [
            '--input-type', 'S3',
            '--input-name', 'source_bucket',
            '--output-type', 'LOCAL_DISK']
        with self.assertRaises(SystemExit):
            command_line_parser.parse_command_line(test_args)
        self.assertRegexpMatches(
            mock_stderr.getvalue(),
            r"the following arguments are required: --output-name")

    @patch('sys.stderr', new_callable=StringIO)
    def test_input_type_valid(self, mock_stderr):
        test_args = [
            '--input-type', 'WEB'
            '--input-name', 'http://host.domain.tld/directory',
            '--output-type', 'LOCAL_DISK',
            '--output-name', '/path/to/the/files']
        with self.assertRaises(SystemExit):
            command_line_parser.parse_command_line(test_args)
        self.assertRegexpMatches(
            mock_stderr.getvalue(),
            r"--input-type {LOCAL_DISK,S3}")

    @patch('sys.stderr', new_callable=StringIO)
    def test_output_type_valid(self, mock_stderr):
        test_args = [
            '--input-type', 'LOCAL_DISK',
            '--input-name', '/path/to/the/files',
            '--output-type', 'RDS',
            '--output-name', 'server=127.0.0.1;uid=root;pwd=12345;database=test']
        with self.assertRaises(SystemExit):
            command_line_parser.parse_command_line(test_args)
        self.assertRegexpMatches(
            mock_stderr.getvalue(),
            r"--output-type\s+{LOCAL_DISK,S3,DYNAMO_DB}")


if __name__ == '__main__':
    unittest.main()
