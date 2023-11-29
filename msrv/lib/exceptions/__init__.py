class EmptyPromptError(Exception):
    def __init__(self, message="Prompt must contain at least one character."):
        self.message = message
        super().__init__(self.message)


class Error200(Exception):
    def __init__(self, message="Received status 200 but with error included"):
        self.message = message
        super().__init__(self.message)
