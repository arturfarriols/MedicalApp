from .resources_enum import ResourceType as RT

class ResourceNotFoundException(Exception):
    def __init__(self, resource_type):
        super().__init__(f"Resource not found: {resource_type}")
        self.resource_type = resource_type