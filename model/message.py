from abc import ABCMeta, abstractmethod
import logging


class MessageType():
    HELLO = 'hello'
    RECONNECT_URL = 'reconnect_url'
    TEXT = 'message'
    TEAM_JOIN = 'team_join'
    ERROR = 'error'
    

class BaseMessage(object):
    __metaclass__ = ABCMeta

    def __init__(self, jsonObj):
        self.type = jsonObj['type']



class HelloMessage(BaseMessage):
    def __init__(self, jsonObj):
        super(HelloMessage, self).__init__(jsonObj)


class ReconnectUrlMessage(BaseMessage):
    def __init__(self, jsonObj):
        super(ReconnectUrlMessage, self).__init__(jsonObj)
        self.url = jsonObj['url']


class TextMessage(BaseMessage):
    def __init__(self, jsonObj):
        super(TextMessage, self).__init__(jsonObj)
        self.text = jsonObj['text']
        self.channel_key = jsonObj['channel']
        self.user_key = jsonObj['user']
        self.ts = jsonObj['ts']

    
class TeamJoinMessage(BaseMessage):
    def __init__(self, jsonObj):
        super(TeamJoinMessage, self).__init__(jsonObj)
        self.user_keys = jsonObj['user']


class ErrorMessage(BaseMessage):
    def __init__(self, jsonObj):
        super(ErrorMessage, self).__init__(jsonObj)
        self.error_code = jsonObj['code']
        self.error_message = jsonObj['msg']
