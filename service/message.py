import logging
import simplejson as json

from model.message import *
from exception.message import MessageParseException

class MessageParser():
    def __init__(self):
        self.MESSAGE_MAPPING = {
            MessageType.HELLO : HelloMessage,
            MessageType.RECONNECT_URL : ReconnectUrlMessage,
            MessageType.TEXT : TextMessage,
            MessageType.TEAM_JOIN : TextMessage,
            MessageType.ERROR : ErrorMessage,
            }
    
    def parse(self, jsonText):
        jsonObj = json.loads(jsonText)
        logging.debug(jsonObj)

        handle_class = self.MESSAGE_MAPPING.get(jsonObj.get('type'))
        if not handle_class:
            raise MessageParseException('no parsable message. type:{}'.format(jsonObj.get('type')))

        try:
            return handle_class(jsonObj)
        except:
            raise MessageParseException('format for message type:{} is invalid'.format(jsonObj.get('type')))
