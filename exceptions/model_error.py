class ModelErrorException(Exception):
    def __init__(self, error_type):
        super().__init__(f"Model Error")
        self.error_type = error_type