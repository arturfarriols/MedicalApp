# from .resource_not_found import ResourceNotFoundException
# from . model_error import ModelErrorException
# from .invalid_data import InvalidDataException
# from .resources_enum import ResourceType as RT
from .exceptions_core import *

CUSTOM_EXCEPTION_MESSAGES = {
    ResourceNotFoundException: {
        RT.VIDEO_PATH: {
            'text': "The chosen video is no longer available. Check if it has been modified",
            'title': "Video Not Available",
        },
        RT.VIDEO: {
            'text': "There is no video to analyze",
            'title': "Any video chosen",
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
        ME.INSTANTIATION: {
            'text': "The analysis model couldn't be loaded properly",
            'title': "Model Error",
        },
        ME.INFERENCE: {
            'text': "The images couldn't be analyzed by the model",
            'title': "Model Error",
        },
    },
    VideoErrorException: {
        'text': "Video {video_name} couldn't be processed",
        'title': "Video Error"
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
    VideoErrorException: "handle_video_error"
}
