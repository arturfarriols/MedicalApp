class ModelErrorException(Exception):
    def __init__(self, resource_type):
        super().__init__(f"Model Error")