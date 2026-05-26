import json
import queue
from unittest.mock import MagicMock

import pytest

from config import AppConfig
from services.speech_listener import SpeechListener


@pytest.fixture
def config():
    return AppConfig(
        vosk_model_path="mock_model",
        queue_timeout=0.01,
        device_index=0,
    )


@pytest.fixture
def mock_recognizer():
    return MagicMock()


@pytest.fixture
def listener(mocker, config, mock_recognizer):
    mocker.patch(
        "services.speech_listener.Model",
        return_value=MagicMock(),
    )

    mocker.patch(
        "services.speech_listener.KaldiRecognizer",
        return_value=mock_recognizer,
    )

    return SpeechListener(
        output_queue=queue.Queue(),
        config=config,
    )


def test_init__valid_data__initializes_components(listener):
    assert listener.daemon is True
    assert isinstance(listener.output_queue, queue.Queue)
    assert isinstance(listener.audio_queue, queue.Queue)
    assert not listener.stop_event.is_set()
    assert listener.model is not None
    assert listener.recognizer is not None


def test_audio_callback__valid_data__puts_audio_into_queue(listener):
    audio_data = b"audio-bytes"

    listener.audio_callback(
        indata=audio_data,
        frames=1,
        time_info=None,
        status=None,
    )

    assert listener.audio_queue.get_nowait() == audio_data


def test_audio_callback__overflow__logs_status_warning(listener, mocker):
    logger_warning = mocker.patch("services.speech_listener.logger.warning")

    listener.audio_callback(
        indata=b"audio",
        frames=1,
        time_info=None,
        status="overflow",
    )

    logger_warning.assert_called_once_with(
        "Audio status: %s",
        "overflow",
    )


def test_audio_callback__full_queue__drops_chunk(listener, mocker):
    logger_warning = mocker.patch("services.speech_listener.logger.warning")

    listener.audio_queue = MagicMock()
    listener.audio_queue.put_nowait.side_effect = queue.Full

    listener.audio_callback(
        indata=b"audio",
        frames=1,
        time_info=None,
        status=None,
    )

    logger_warning.assert_called_once_with("Audio queue full, dropping chunk")


def test_recognize_speech__valid_data__puts_text_into_output_queue(
    listener,
    mock_recognizer,
):
    mock_recognizer.AcceptWaveform.return_value = True

    mock_recognizer.Result.return_value = json.dumps({"text": "hello world"})

    listener.audio_queue.put(b"audio")

    listener.stop_event = MagicMock()
    listener.stop_event.is_set.side_effect = [False, True]

    listener.recognize_speech()

    assert listener.output_queue.get_nowait() == "hello world"


def test_recognize_speech__empty_text__does_not_enqueue_output(
    listener,
    mock_recognizer,
):
    mock_recognizer.AcceptWaveform.return_value = True

    mock_recognizer.Result.return_value = json.dumps({"text": ""})

    listener.audio_queue.put(b"audio")

    listener.stop_event = MagicMock()
    listener.stop_event.is_set.side_effect = [False, True]

    listener.recognize_speech()

    assert listener.output_queue.empty()


def test_recognize_speech__incomplete_waveform__does_not_enqueue_output(
    listener,
    mock_recognizer,
):
    mock_recognizer.AcceptWaveform.return_value = False

    listener.audio_queue.put(b"audio")

    listener.stop_event = MagicMock()
    listener.stop_event.is_set.side_effect = [False, True]

    listener.recognize_speech()

    assert listener.output_queue.empty()


def test_recognize_speech__empty_audio__does_not_enqueue_output(
    listener,
):
    listener.stop_event = MagicMock()
    listener.stop_event.is_set.side_effect = [False, True]

    listener.recognize_speech()

    assert listener.output_queue.empty()


def test_run__valid_stream__starts_audio_stream(
    listener,
    mocker,
):
    mock_stream = mocker.patch("services.speech_listener.sd.RawInputStream")

    recognize_speech = mocker.patch.object(
        listener,
        "recognize_speech",
    )

    listener.run()

    mock_stream.assert_called_once_with(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1,
        device=listener.config.device_index,
        callback=listener.audio_callback,
    )

    recognize_speech.assert_called_once()


def test_run__invalid_stream__logs_exception(
    listener,
    mocker,
):
    mocker.patch(
        "services.speech_listener.sd.RawInputStream",
        side_effect=Exception("stream failed"),
    )

    logger_exception = mocker.patch("services.speech_listener.logger.exception")

    listener.run()

    logger_exception.assert_called_once_with("Audio stream error")


def test_stop__called__sets_stop_event(listener):
    listener.stop()

    assert listener.stop_event.is_set()
