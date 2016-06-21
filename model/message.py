from abc import ABCMeta, abstractmethod
import logging


class BaseMessage(object):
    __metaclass__ = ABCMeta

    def __init__(self, jsonObj):
        self.message_type = jsonObj['type']

    @abstractmethod
    def process(self):
        pass

class HelloMessage(BaseMessage):
    def __init__(self, jsonObj):
        super(HelloMessage, self).__init__(jsonObj)

    def process(self):
        super(HelloMessage, self).process()
        logging.info('RTM initiailzed')


class TextMessage(BaseMessage):
    def __init__(self, jsonObj):
        super(TextMessage, self).__init__(jsonObj)
        self.text = jsonObj['text']

    def process(self):
        super(TextMessage, self).process()
        logging.debug('text message')

    
class TeamJoinMessage(BaseMessage):
    def __init__(self, jsonObj):
        super(TeamJoinMessage, self).__init__(jsonObj)
        self.user_keys = jsonObj['user']

    def process(self):
        super(TeamJoinMessage, self).process()
        logging.debug('team join message')
