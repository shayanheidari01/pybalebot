class RPCError(Exception):
    def __init__(self, message, code=None):
        self.message = message
        self.code = code
        super().__init__(self.message)
    
    def __str__(self):
        if self.code is not None:
            return f'RPCError {self.code}: {self.message}'
        else:
            return f'RPCError: {self.message}'