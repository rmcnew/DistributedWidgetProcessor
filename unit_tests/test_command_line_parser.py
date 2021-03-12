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
            r"--input-type {LOCAL_DISK,S3,SQS}")

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
