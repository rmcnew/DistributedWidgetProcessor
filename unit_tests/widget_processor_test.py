import unittest
import json
import widget_processor


class WidgetProcessorTestCases(unittest.TestCase):
    def test_create_widget(self):
        self.maxDiff = None
        widget_str = """{"type": "create", "requestId": "6f6121c7-14d6-4d0a-a431-9f1a6dde8808",
                      "widgetId": "7f0bfd22-876f-42f2-937d-cdf048caec2a", "owner": "Mary Matthews", "label": "ET",
                      "description": "DYNJLGBLSLEZLEJECEVLLXUMNPSJAEYVNECKBQFIHPAOMCSVRHZINZWXDXQFOTXDVCAGSAYK",
                      "otherAttributes": [{"name": "color", "value": "blue"}, {"name": "size", "value": "143"},
                                          {"name": "size-unit", "value": "cm"}, {"name": "height", "value": "379"},
                                          {"name": "width-unit", "value": "cm"}, {"name": "length-unit", "value": "cm"},
                                          {"name": "price", "value": "31.84"}, {"name": "quantity", "value": "650"},
                                          {"name": "note", "value": "EFCQGMBMWWRVXGQUZXUFWSSOUSXZSFEDMGEQISTGTKRAOFAFFSZVJWTLJYPMZWGRSULXEZDSHOXQEMBQPGXBCWSJABNPNEDMTPFJZMXLBOHOJCHLBVGTUDBEJDMOWNQHTTIYHMVPYWSUXYUBPTY"}]}"""
        widget = json.loads(widget_str)
        widget_to_store = widget_processor.create_widget('X', widget)
        widget_to_store_string = json.dumps(widget_to_store)
        expected_widget = '{"widget_id": "7f0bfd22-876f-42f2-937d-cdf048caec2a", "owner": "Mary-Matthews", "label": "ET", "description": "DYNJLGBLSLEZLEJECEVLLXUMNPSJAEYVNECKBQFIHPAOMCSVRHZINZWXDXQFOTXDVCAGSAYK", "otherAttributes": [{"name": "color", "value": "blue"}, {"name": "size", "value": "143"}, {"name": "size-unit", "value": "cm"}, {"name": "height", "value": "379"}, {"name": "width-unit", "value": "cm"}, {"name": "length-unit", "value": "cm"}, {"name": "price", "value": "31.84"}, {"name": "quantity", "value": "650"}, {"name": "note", "value": "EFCQGMBMWWRVXGQUZXUFWSSOUSXZSFEDMGEQISTGTKRAOFAFFSZVJWTLJYPMZWGRSULXEZDSHOXQEMBQPGXBCWSJABNPNEDMTPFJZMXLBOHOJCHLBVGTUDBEJDMOWNQHTTIYHMVPYWSUXYUBPTY"}]}'
        self.assertEqual(widget_to_store_string, expected_widget)


if __name__ == '__main__':
    unittest.main()
