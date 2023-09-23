class InvalidDataException(Exception):
    def __init__(self, data_type, accepted_formats):
        super().__init__(f"Invalid data: {data_type}")
        self.data_type = data_type
        self.accepted_formats = accepted_formats