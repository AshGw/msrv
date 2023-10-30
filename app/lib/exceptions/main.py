class EmptyPromptError(Exception):
    def __init__(self, message="Prompt must contain at least one character."):
        self.message = message
        super().__init__(self.message)
