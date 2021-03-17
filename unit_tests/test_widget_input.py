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
import widget_input


class WidgetInputTestCases(unittest.TestCase):
    def test_get_random_queue_name(self):
        q_name1 = widget_input.get_random_queue_name()
        q_name2 = widget_input.get_random_queue_name()
        print(f"{q_name1} is probably not equal to {q_name2}")
        self.assertNotEqual(q_name1, q_name2)


if __name__ == '__main__':
    unittest.main()
