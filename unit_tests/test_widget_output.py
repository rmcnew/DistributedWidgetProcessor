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

import json
import unittest

import widget_output


class WidgetOutputTestCases(unittest.TestCase):
    def test_convert_widget_to_dynamo_db_schema(self):
        self.maxDiff = None
        widget = json.loads('{"widget_id": "d2d540b0-5999-4d43-8f09-b8f528a0f032", "owner": "Sue-Smith", "label": "G", "description": "AYGDDAZYZTGPL", "otherAttributes": [{"name": "color", "value": "blue"}, {"name": "height-unit", "value": "cm"}, {"name": "width", "value": "353"}, {"name": "width-unit", "value": "cm"}, {"name": "rating", "value": "3.345904"}, {"name": "vendor", "value": "CTXCQKZRH"}, {"name": "note", "value": "RQOCJENLLWHZUUTRDDXPKWTDRDQJMRKOKYBIVWFNTGMXFDWSIYZFCRMKMBQEGZBJLDWCIOMXHQJHYJRCZBRRRIRTOISLCJPJBYXTDTNMPQTYCPDEDBYJUMRTBRRIKXMAINMONUWMRCFJOGPCUUGVUMNAJMKKETBCCXYYKKUMLBBKYBEFWUCQPWMJPBLKNXKKBFJBYEXRSIVMCTBICSSTGZJGJSYMQEIEGHSOSISZNXTTHEWPEYBQACLCOOVJXBYSCFIMFVWISSHLCODAWWXXHXUJKVWPJEBYFATGBGIXDJJCXSDRWJRKHZJCNBPRNGSMRLBXJLTYLK"}]}')
        ddb_widget = widget_output.convert_widget_to_dynamo_db_schema('X', widget)
        ddb_widget_str = json.dumps(ddb_widget)
        expected_ddb_widget_str = '{"widget_id": {"S": "d2d540b0-5999-4d43-8f09-b8f528a0f032"}, "owner": {"S": "Sue-Smith"}, "label": {"S": "G"}, "description": {"S": "AYGDDAZYZTGPL"}, "color": {"S": "blue"}, "height-unit": {"S": "cm"}, "width": {"S": "353"}, "width-unit": {"S": "cm"}, "rating": {"S": "3.345904"}, "vendor": {"S": "CTXCQKZRH"}, "note": {"S": "RQOCJENLLWHZUUTRDDXPKWTDRDQJMRKOKYBIVWFNTGMXFDWSIYZFCRMKMBQEGZBJLDWCIOMXHQJHYJRCZBRRRIRTOISLCJPJBYXTDTNMPQTYCPDEDBYJUMRTBRRIKXMAINMONUWMRCFJOGPCUUGVUMNAJMKKETBCCXYYKKUMLBBKYBEFWUCQPWMJPBLKNXKKBFJBYEXRSIVMCTBICSSTGZJGJSYMQEIEGHSOSISZNXTTHEWPEYBQACLCOOVJXBYSCFIMFVWISSHLCODAWWXXHXUJKVWPJEBYFATGBGIXDJJCXSDRWJRKHZJCNBPRNGSMRLBXJLTYLK"}}'
        self.assertEqual(ddb_widget_str, expected_ddb_widget_str)


    def test_flatten_unflatten_widget(self):
        self.maxDiff = None
        widget_str = '{"widget_id": "d2d540b0-5999-4d43-8f09-b8f528a0f032", "owner": "Sue-Smith", "label": "G", "description": "AYGDDAZYZTGPL", "otherAttributes": [{"name": "color", "value": "blue"}, {"name": "height-unit", "value": "cm"}, {"name": "width", "value": "353"}, {"name": "width-unit", "value": "cm"}, {"name": "rating", "value": "3.345904"}, {"name": "vendor", "value": "CTXCQKZRH"}, {"name": "note", "value": "RQOCJENLLWHZUUTRDDXPKWTDRDQJMRKOKYBIVWFNTGMXFDWSIYZFCRMKMBQEGZBJLDWCIOMXHQJHYJRCZBRRRIRTOISLCJPJBYXTDTNMPQTYCPDEDBYJUMRTBRRIKXMAINMONUWMRCFJOGPCUUGVUMNAJMKKETBCCXYYKKUMLBBKYBEFWUCQPWMJPBLKNXKKBFJBYEXRSIVMCTBICSSTGZJGJSYMQEIEGHSOSISZNXTTHEWPEYBQACLCOOVJXBYSCFIMFVWISSHLCODAWWXXHXUJKVWPJEBYFATGBGIXDJJCXSDRWJRKHZJCNBPRNGSMRLBXJLTYLK"}]}'
        widget = json.loads(widget_str)
        flat_widget = widget_output.flatten_widget('X', widget)
        flat_widget_str = json.dumps(flat_widget)
        expected_flat_widget_str = '{"widget_id": "d2d540b0-5999-4d43-8f09-b8f528a0f032", "owner": "Sue-Smith", "label": "G", "description": "AYGDDAZYZTGPL", "color": "blue", "height-unit": "cm", "width": "353", "width-unit": "cm", "rating": "3.345904", "vendor": "CTXCQKZRH", "note": "RQOCJENLLWHZUUTRDDXPKWTDRDQJMRKOKYBIVWFNTGMXFDWSIYZFCRMKMBQEGZBJLDWCIOMXHQJHYJRCZBRRRIRTOISLCJPJBYXTDTNMPQTYCPDEDBYJUMRTBRRIKXMAINMONUWMRCFJOGPCUUGVUMNAJMKKETBCCXYYKKUMLBBKYBEFWUCQPWMJPBLKNXKKBFJBYEXRSIVMCTBICSSTGZJGJSYMQEIEGHSOSISZNXTTHEWPEYBQACLCOOVJXBYSCFIMFVWISSHLCODAWWXXHXUJKVWPJEBYFATGBGIXDJJCXSDRWJRKHZJCNBPRNGSMRLBXJLTYLK"}'
        self.assertEqual(expected_flat_widget_str, flat_widget_str)
        unflattened_widget = widget_output.unflatten_widget('Y', flat_widget)
        self.assertEqual(widget, unflattened_widget)


if __name__ == '__main__':
    unittest.main()
