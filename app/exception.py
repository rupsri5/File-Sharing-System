class InputException(Exception):
    def __init__(self, message='Invalid input'):
        self.message = message
        super().__init__(self.message)

class TokenException(Exception):
    def __init__(self, message='Invalid special token.'):
        self.message = message
        super().__init__(self.message)