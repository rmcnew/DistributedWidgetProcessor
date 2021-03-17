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

# Constants that are shared throughout the program to avoid typographical errors

BODY = "Body"
CODE = "Code"
COMPLETED_LOCATION = "completed"
CONTENTS = "Contents"
CREATE = "create"
CS5260_REQUESTS_SQS_URL = "https://sqs.us-east-1.amazonaws.com/546700818303/cs5260-requests"
DELETE = "delete"
DESCRIPTION = "description"
DIST_BUCKET = "usu-cs5260-homework-assignment-two-dist"
DYNAMO_DB = "DYNAMO_DB"
ERROR = "Error"
ERROR_LOCATION = "error"
KEY = "Key"
KEY_COUNT = "KeyCount"
LABEL = "label"
LOCAL_DISK = "LOCAL_DISK"
MESSAGES = 'Messages'
NAME = "name"
NO_SUCH_KEY = 'NoSuchKey'
NOT_FOUND = "404"
OWNER = "owner"
OTHER_ATTRIBUTES = "otherAttributes"
PROCESSING_LOCATION = "processing"
QUEUE_URL = 'QueueUrl'
RECEIPT_HANDLE = 'ReceiptHandle'
RETRY_PROCESSING_COUNT = 3
REQUEST_BUCKET = "usu-cs5260-homework-assignment-two-requests"
REQUEST_ID = "requestId"
S = 'S'
S3 = "S3"
S3_MAX_KEYS_TO_LIST = 30
SQS = "SQS"
SQS_MESSAGE_COUNT = 4
SQS_WAIT_TIME = 10  # seconds
TYPE = "type"
UPDATE = "update"
UTF8 = "utf-8"
VALUE = "value"
WEB_BUCKET = "usu-cs5260-homework-assignment-two-web"
WIDGETID = "widgetId"
WIDGET_ID = "widget_id"
WIDGETS = "widgets"
# structures using the above constants
NON_OTHER_ATTRIBUTES = [WIDGET_ID, OWNER, LABEL, DESCRIPTION]
