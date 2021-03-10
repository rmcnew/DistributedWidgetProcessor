import unittest
import json
import tempfile
import uuid
from pathlib import Path
from constants import *
import widget_output


class WidgetOutputTestCases(unittest.TestCase):
    def test_convert_widget_to_dynamo_db_schema(self):
        self.maxDiff = None
        widget = json.loads('{"widget_id": "d2d540b0-5999-4d43-8f09-b8f528a0f032", "owner": "Sue-Smith", "label": "G", "description": "AYGDDAZYZTGPL", "otherAttributes": [{"name": "color", "value": "blue"}, {"name": "height-unit", "value": "cm"}, {"name": "width", "value": "353"}, {"name": "width-unit", "value": "cm"}, {"name": "rating", "value": "3.345904"}, {"name": "vendor", "value": "CTXCQKZRH"}, {"name": "note", "value": "RQOCJENLLWHZUUTRDDXPKWTDRDQJMRKOKYBIVWFNTGMXFDWSIYZFCRMKMBQEGZBJLDWCIOMXHQJHYJRCZBRRRIRTOISLCJPJBYXTDTNMPQTYCPDEDBYJUMRTBRRIKXMAINMONUWMRCFJOGPCUUGVUMNAJMKKETBCCXYYKKUMLBBKYBEFWUCQPWMJPBLKNXKKBFJBYEXRSIVMCTBICSSTGZJGJSYMQEIEGHSOSISZNXTTHEWPEYBQACLCOOVJXBYSCFIMFVWISSHLCODAWWXXHXUJKVWPJEBYFATGBGIXDJJCXSDRWJRKHZJCNBPRNGSMRLBXJLTYLK"}]}')
        ddb_widget = widget_output.convert_widget_to_dynamo_db_schema('X', widget)
        ddb_widget_str = json.dumps(ddb_widget)
        expected_ddb_widget_str = '{"widget_id": {"S": "d2d540b0-5999-4d43-8f09-b8f528a0f032"}, "owner": {"S": "Sue-Smith"}, "label": {"S": "G"}, "description": {"S": "AYGDDAZYZTGPL"}, "color": {"S": "blue"}, "height-unit": {"S": "cm"}, "width": {"S": "353"}, "width-unit": {"S": "cm"}, "rating": {"S": "3.345904"}, "vendor": {"S": "CTXCQKZRH"}, "note": {"S": "RQOCJENLLWHZUUTRDDXPKWTDRDQJMRKOKYBIVWFNTGMXFDWSIYZFCRMKMBQEGZBJLDWCIOMXHQJHYJRCZBRRRIRTOISLCJPJBYXTDTNMPQTYCPDEDBYJUMRTBRRIKXMAINMONUWMRCFJOGPCUUGVUMNAJMKKETBCCXYYKKUMLBBKYBEFWUCQPWMJPBLKNXKKBFJBYEXRSIVMCTBICSSTGZJGJSYMQEIEGHSOSISZNXTTHEWPEYBQACLCOOVJXBYSCFIMFVWISSHLCODAWWXXHXUJKVWPJEBYFATGBGIXDJJCXSDRWJRKHZJCNBPRNGSMRLBXJLTYLK"}}'
        self.assertEqual(ddb_widget_str, expected_ddb_widget_str)

    def test_create_local_disk_output_directories(self):
        tmp_dir = tempfile.gettempdir()
        tmp_output_dir_name = uuid.uuid4()
        output_dir = Path("{}/{}".format(tmp_dir, tmp_output_dir_name))
        owner = "Big_Bad_John"
        widget_output.create_local_disk_output_directories('X', output_dir, owner)
        self.assertTrue(Path("{}/{}/{}".format(tmp_dir, tmp_output_dir_name, owner)).exists())



if __name__ == '__main__':
    unittest.main()
