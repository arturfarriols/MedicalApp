from .resource_not_found import ResourceNotFoundException
from . model_error import ModelErrorException
from .invalid_data import InvalidDataException
from .resources_enum import ResourceType as RT

CUSTOM_EXCEPTION_MESSAGES = {
    ResourceNotFoundException: {
        RT.VIDEO: {
            'text': "The chosen video is no longer available. Check if it has been modified",
            'title': "Video Not Available",
        },
        RT.RESULTS: {
            'text': "An analysis must be finished before exporting its results",
            'title': "No Results To Export",
        },

    },
    InvalidDataException: {
        'text': """Invalid data format: {details}
Available formats are: {available_formats}""",
        'title': "Invalid Data",
    },
    ModelErrorException: {
        'text': "Model error: {error_message}",
        'title': "Model Error",
    },
    Exception: {
        'text': "An error occurred: {error_message}",
        'title': "Error",
    }
}

DEFAULT_EXCEPTION_MESSAGE = {
    'text': "An error occurred",
    'title': "Error",    
}

EXCEPTION_FUNCTIONS = {
    ResourceNotFoundException: "handle_resource_not_found",
    InvalidDataException: "handle_invalid_data",
    ModelErrorException: "handle_model_error",
}
