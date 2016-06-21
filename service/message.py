import simplejson as json

from model.message import *

class MessageParser():
    def __init__(self):
        self.MESSAGE_MAPPING = dict(
            hello = HelloMessage,
            message = TextMessage,
            )
    
    def parse(self, jsonText):
        jsonObj = json.loads(jsonText)

        handle_class = self.MESSAGE_MAPPING.get(jsonObj['type'])
        if not handle_class:
            raise Exception('no parsable message')

        return handle_class(jsonObj)
