class MessageParseException(Exception):
    def __init__(self, msg):
        super(MessageParseException, self).__init__(msg)
