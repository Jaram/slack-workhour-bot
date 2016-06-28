class BurgerKingException(Exception):
    def __init__(self, msg):
        super(BurgerKingException, self).__init__(msg)
