import pytest
from unittest.mock import patch, MagicMock, call

from models.model_controller import ModelController
from models.segmentation_model_pytorch import SegmentationModel
from models.data_manager import DataManager

from exceptions.exceptions_core import *

@pytest.fixture
def model_controller_fixture():
    return ModelController()

def test_initiate_models_successful(model_controller_fixture):
    # Mock the SegmentationModel class to avoid actual instantiation
    SegmentationModel.__init__ = MagicMock(return_value=None)

    # Mock the DataManager class to avoid actual instantiation
    DataManager.__init__ = MagicMock(return_value=None)

    # Call the initiate_models method
    model_controller_fixture.initiate_models()

    # Ensure that SegmentationModel.__init__ was called with the expected argument
    SegmentationModel.__init__.assert_called_once_with("main")

    # Add assertions for any expected behavior after calling initiate_models
    assert model_controller_fixture.model is not None  # Check that the 'model' attribute is not None
    assert not model_controller_fixture.finished_processing  # Check that 'finished_processing' is False

def test_initiate_models_exception(model_controller_fixture):
    # Create an instance of ModelErrorException with the desired message
    # exception_instance = ModelErrorException(ME.INSTANTIATION)
    exception_instance = Exception("Instantiation error")

    # Mock SegmentationModel.__init__ to raise the exception instance
    SegmentationModel.__init__ = MagicMock(side_effect=exception_instance)

    # Call the initiate_models method within a context manager to check for the expected exception
    with pytest.raises(ModelErrorException) as excinfo:
        model_controller_fixture.initiate_models()

    # Check if the exception message matches your expectation
    assert isinstance(excinfo.value, (ModelErrorException))

    assert excinfo.value.error_type == ME.INSTANTIATION

# Test case for the final_process_videos method
def test_final_process_videos_successful(model_controller_fixture):
    # Create a list of sample videos for testing
    sample_videos = ['video1.mp4', 'video2.mp4']
    expected_results = [[{'LVID': 0.5, }, 'video1.mp4'], [{'LVID': 0.5, }, 'video2.mp4']]

    model_controller_fixture.final_process_video = MagicMock()

    # Mock the final_process_video method to return sample data
    model_controller_fixture.final_process_video.return_value = ({'metric': 42}, 'video_1.mp4')

    # Create a MagicMock for the percentage_actualized signal
    percentage_actualized_signal = MagicMock()
    model_controller_fixture.percentage_actualized = percentage_actualized_signal

    # Create a MagicMock for the results_obtained signal
    results_obtained_signal = MagicMock()
    model_controller_fixture.results_obtained = results_obtained_signal


    # Create a MagicMock for the thread attribute
    thread_mock = MagicMock()
    model_controller_fixture.thread = thread_mock

    # Mock the stop_execution method of the thread
    thread_mock.stop_execution = MagicMock()

    # Mock the CHI.calculateAll method
    with patch('models.calculate_health_indicators.calculateAll') as mock_calculateAll:
        mock_calculateAll.return_value = {'LVID': 0.5}

        # Call the final_process_videos method
        results = model_controller_fixture.final_process_videos(sample_videos)

    # Assert that the results are not empty
    assert results

    # Assert that the results contain lists with health indicators and video names
    for result in results:
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], dict)  # Assuming health_indicators is a dictionary
        assert isinstance(result[1], str)  # Assuming video is a string

    # Assert that the processing_videos flag is set to False after processing
    assert not model_controller_fixture.processing_videos

    # Assert that the finished_processing flag is set to True after processing
    assert model_controller_fixture.finished_processing

    # Verify that final_process_video was called for each video
    assert model_controller_fixture.final_process_video.call_count == len(sample_videos)

    # Verify that the percentage_actualized signal was emitted with the expected values
    # model_controller_fixture.percentage_actualized.assert_called_once()
    # expected_calls = [call(int(percentage)) for percentage in range(0, 101)]
    # percentage_actualized_signal.assert_has_calls(expected_calls, any_order=True)

    # Verify that the results_obtained signal was emitted with the expected results
    # results_obtained_signal.assert_called_once()
    # results_obtained_signal.assert_called_once_with({'LVID': 0.5})
    # Assert that execution_results attribute is set correctly
    assert model_controller_fixture.execution_results == expected_results

def test_final_process_videos_exception(model_controller_fixture):
    # Create a list of sample videos for testing
    sample_videos = ['video1.mp4', 'video2.mp4']

    model_controller_fixture.final_process_video = MagicMock()

    # Mock the final_process_video method to raise a Exception
    model_controller_fixture.final_process_video.side_effect = Exception("Inference error")

    # Test that ModelErrorException 
    with pytest.raises(Exception) as excinfo:
        model_controller_fixture.final_process_videos(sample_videos)

    # Verify that the caught exception is either ModelErrorException
    assert isinstance(excinfo.value, (ModelErrorException))

    assert excinfo.value.error_type == ME.INFERENCE

def test_import_video_successful(model_controller_fixture):
    # Mock the data_manager's import_video method to return a sample video path
    expected_video_path = 'video1.mp4'
    model_controller_fixture.data_manager.import_video = MagicMock(return_value=expected_video_path)

    # Call the import_video method
    result = model_controller_fixture.import_video()

    # Assert that the result is the expected video path
    assert result == expected_video_path

    # Verify that the data_manager's import_video method was called
    model_controller_fixture.data_manager.import_video.assert_called_once()

def test_import_video_with_exceptions(model_controller_fixture):
    # Mock the data_manager's import_video method to raise an exception
    model_controller_fixture.data_manager.import_video = MagicMock(side_effect=InvalidDataException(RT.VIDEO.value, ['mp4']))

    # Call the import_video method within a pytest.raises context manager to catch the exception
    with pytest.raises(Exception) as excinfo:
        model_controller_fixture.import_video()

    # Verify that the caught exception has the expected error message
    # assert str(excinfo.value) == "Video import failed"
    assert isinstance(excinfo.value, (InvalidDataException))

    # Verify that the data_manager's import_video method was called
    model_controller_fixture.data_manager.import_video.assert_called_once()

def test_export_results_successful(model_controller_fixture):
    # Mock the data_manager's export_data method
    model_controller_fixture.data_manager.export_data = MagicMock()

    # Set execution_results to a non-empty value
    model_controller_fixture.execution_results = [{'metric': 42}, 'video_1.mp4']

    # Call the export_results method
    model_controller_fixture.export_results()

    # Verify that the data_manager's export_data method was called with the expected argument
    model_controller_fixture.data_manager.export_data.assert_called_once_with(model_controller_fixture.execution_results)

def test_export_results_exception(model_controller_fixture):
    # Mock the data_manager's export_data method
    model_controller_fixture.data_manager.export_data = MagicMock()

    # Set execution_results to None
    model_controller_fixture.execution_results = None

    # Call the export_results method within a pytest.raises context manager to catch the exception
    with pytest.raises(Exception) as excinfo:
        model_controller_fixture.export_results()

    # Verify that the caught exception has the expected error type
    assert isinstance(excinfo.value, ResourceNotFoundException)
    assert excinfo.value.resource_type == RT.RESULTS

    # Verify that the data_manager's export_data method was not called
    model_controller_fixture.data_manager.export_data.assert_not_called()