# -*- coding:utf-8 -*-

import logging
import websocket

from slacker import Slacker

from model.message import MessageType
from service.message import MessageParser
from exception.message import MessageParseException

class UserInfo():
    def __init__(self, user_key, user_name):
        self.user_key = user_key
        self.user_name = user_name


class ChannelInfo():
    def __init__(self, channel_key, channel_name):
        self.channel_key = channel_key
        self.channel_name = channel_name


class Connection():
    def __init__(self, url):
        self.connection = websocket.WebSocket()
        self.reconnect_url = url
        self.message_parser = MessageParser()

        self._connect()

    def _connect(self):
        self.connection.connect(self.reconnect_url)

    def get_message(self):
        try:
            recved_data = self.connection.recv()
            return self.message_parser.parse(recved_data)
        except MessageParseException as e:
            logging.info(e)
            return None
        except Exception:
            self._connect()
            return None
        

class WorkHourBot():
    def __init__(self, api_key):
        self.api_key = api_key
        self.slack = Slacker(api_key)
        self.user_infos = dict()
        self.channel_infos = dict()
        self.connection = None
        
        self._init_message_handler()
        
    def _init_message_handler(self):
        self.message_handler = {
            MessageType.HELLO : self._handle_hello_message,
            MessageType.RECONNECT_URL : self._handle_reconnect_url_message,
            MessageType.TEXT : self._handle_text_message
            }
            

    def run(self):
        server_url = self._rtm_start()

        self.connection = Connection(server_url)
        # main loop
        while True:
            message = self.connection.get_message()
            if message:
                self._handle_message(message)
            
    def _rtm_start(self):
        response = self.slack.rtm.start()
        for userinfo_dict in response.body['users']:
            self.user_infos[userinfo_dict['id']] = UserInfo(userinfo_dict['id'], userinfo_dict['real_name'])
        for channelinfo_dict in response.body['channels']:
            channel_key = channelinfo_dict['id']
            self.channel_infos[channel_key] = ChannelInfo(channel_key, channelinfo_dict['name'])

        return response.body['url']
    
    def _handle_message(self, message):
        handler = self.message_handler.get(message.type)
        if not handler:
            raise Exception('no handler for message. type:{}'.format(message.type))
        handler(message)
        
    def _handle_hello_message(self, message):
        logging.info('hello message recved')

    def _handle_reconnect_url_message(self, message):
        logging.info('reconnect url message recved')

    def _handle_text_message(self, message):
        logging.info('text message recved')
        channel_info = self.channel_infos.get(message.channel_key)
        if not channel_info:
            logging.debug('no tracking channel')
            return
        
        if not channel_info.channel_name == 'work_end':
            logging.debug('no tracking channel. channel_name:{}'.format(channel_info.channel_name))
            return

        user_info = self.user_infos.get(message.user_key)
        if not user_info:
            logging.debug('no user info. key:{}'.format(message.user_key))
            return

        if u'!출근' in message.text:
            logging.info("""'{}' said i'm entering the office""".format(user_info.user_name))
        if u'!퇴근' in message.text:
            logging.info("""'{}' said i'm leaving the office""".format(user_info.user_name))

        
