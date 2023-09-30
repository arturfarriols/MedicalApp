import os
import pytest

from qt_core import *
from models import ModelController, SegmentationModel, Video  # Import your actual classes
from exceptions.exceptions_core import * # Import your custom exceptions
from unittest.mock import MagicMock, Mock

def get_parent_path():
    # Get the current script's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate to the parent directory
    parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
    
    return parent_dir

def create_video_common_attributes():
    video_id = 1
    parent_dir = os.path.dirname(get_parent_path())
    filename = "2009-01-01-00-09-01_2009-01-01-00-26-57_1.avi"
    full_path = os.path.join(parent_dir, filename)
    is_automatic = False

    return video_id, full_path, is_automatic

class MockFunctionThread:
    def __init__(self, controller, videos):
        self.controller = controller
        self.videos = videos
        self.status_changed = MagicMock()

    def start(self):
        pass

    def stop_execution(self):
        pass


@pytest.fixture
def correct_video_fixture():
    video_id, full_path, is_automatic = create_video_common_attributes()
    point = QPoint(309, 254)

    # Create an instance of the Video class with its attributes
    video = Video(video_id, full_path)
    video.is_automatic = is_automatic
    video.point = point

    return video

@pytest.fixture
def incorrect_video_fixture():
    video_id, full_path, is_automatic = create_video_common_attributes()
    point = QPoint(35, 254)

    # Create an instance of the Video class with its attributes
    video = Video(video_id, full_path)
    video.is_automatic = is_automatic
    video.point = point

    return video

@pytest.fixture
def model_controller_fixture(monkeypatch):
    monkeypatch.setattr(ModelController, 'percentage_actualized', MagicMock())
    monkeypatch.setattr(ModelController, 'results_obtained', MagicMock())

    model_controller = ModelController()
    model_controller.thread = MockFunctionThread(model_controller, [])
    return model_controller

# Get the current working directory (folder containing main.py)
app_folder = get_parent_path()

# Set the environment variable
os.environ["MY_APP_FOLDER"] = app_folder

def test_correct_video_processing(model_controller_fixture, correct_video_fixture):
    expected_results = {'LVESV': 25.02978760693122, 'LVEDV': 59.45233561679412, 'FS': 29.908458560272987, 'EF': 57.899404039795556, 
'SV': 34.42254800986291, 'CO': 9.938684207576488, 'RWT': 0.5167497867314128, 'IVSd': 1.190563725490196, 'IVSs': 1.683639705882353, 'LVIDs': 2.6179534313725488, 
'LVIDd': 3.735049019607843, 'LVPWd': 0.7395220588235294, 'LVPWs': 1.0471813725490198, 'HR': 288.72598869580514}

    model_controller_fixture.initiate_models()
    assert isinstance(model_controller_fixture.model, SegmentationModel)

    model_controller_fixture.final_process_videos([correct_video_fixture])
    assert(expected_results == model_controller_fixture.execution_results[0][0])

def test_incorrect_video_processing(model_controller_fixture, incorrect_video_fixture):
    expected_results = {'LVESV': -1, 'LVEDV': -1, 'FS': -1, 'EF': -1, 'SV': -1, 'CO': -1, 'RWT': -1, 'IVSs': -1, 'IVSd': -1, 
                        'LVIDs': -1, 'LVIDd': -1, 'LVPWs': -1, 'LVPWd': -1, 'HR': -1}

    model_controller_fixture.initiate_models()
    assert isinstance(model_controller_fixture.model, SegmentationModel)

    model_controller_fixture.final_process_videos([incorrect_video_fixture])
    assert(expected_results == model_controller_fixture.execution_results[0][0])