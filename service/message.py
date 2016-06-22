import simplejson as json

from model.message import *
from exception.message import MessageParseException

class MessageParser():
    def __init__(self):
        self.MESSAGE_MAPPING = {
            MessageType.HELLO : HelloMessage,
            MessageType.RECONNECT_URL : ReconnectUrlMessage,
            MessageType.TEAM_JOIN : TextMessage,
            }
    
    def parse(self, jsonText):
        jsonObj = json.loads(jsonText)

        handle_class = self.MESSAGE_MAPPING.get(jsonObj['type'])
        if not handle_class:
            raise MessageParseException('no parsable message')

        return handle_class(jsonObj)
