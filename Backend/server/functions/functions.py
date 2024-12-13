from enum import Enum
from functions.data_classes import Pipeline, Function_call, Track_characteristic, Time
from fastapi import UploadFile
from io import BytesIO
from functions.utils import pseudo_zip_result
import scipy
import numpy
from typing import Any


def make_pipeline(track: UploadFile, pipeline: Pipeline, to_separate_track: bool) -> BytesIO:
    tracks: list[Audio_track] | Audio_track = Audio_track.from_wav(track, to_separate_track)
    images: list[BytesIO] = [] # has duplication names
    for function in pipeline.pipeline: # TODO: use async to make it faster
        image = Audio_track.use_function(tracks, function)
        if image is not None:
            images.append(image)

    # result audio and images

    return pseudo_zip_result()


class Function_type(int, Enum):
    LOW_PASS      = 0
    HIGH_PASS     = 1
    BAND_PASS     = 2
    NOTCH_FILTER  = 3
    GAIN          = 4
    LEVEL         = 5
    NOISE_FILTER  = 6
    USEFUL_SIGNAL = 7

    TRIM          = 8

    XYZ_DIAGRAM   = 9
    XY_DIAGRAM    = 10

    COPY          = 11


class Audio_track:
    def __init__(self, track: numpy.ndarray, sample_rate: int):
        self.frequency_domain_track = scipy.fft.rfft(track) # maybe incorrect

    @staticmethod
    def use_function(self, tracks: list['Audio_track'], function: Function_call) -> BytesIO | None:
        track_list = tracks
        for i in range(len(function.track) - 1):
            if i >= len(track_list):
                raise ValueError("Track id is out of range")
            track_list = track_list[function.track[i]]

        track_id = function.track[-1]
        if track_id >= len(track_list):
            raise ValueError("Track id is out of range")

        if function.id == Function_type.COPY:
            track_list[track_id] = Audio_track.__copy(track_list[track_id], function.args)
            return None
        else:
            return track_list[track_id].__function_call(function)

    def __function_call(self, function: Function_call) -> BytesIO | None:
        match function.id:
            case Function_type.LOW_PASS:
                self.__low_pass(function.args)
                return None
            case Function_type.HIGH_PASS:
                self.__high_pass(function.args)
                return None
            case Function_type.BAND_PASS:
                self.__band_pass(function.args)
                return None
            case Function_type.NOTCH_FILTER:
                self.__notch_filter(function.args)
                return None
            case Function_type.GAIN:
                self.__gain(function.args)
                return None
            case Function_type.LEVEL:
                self.__level(function.args)
                return None
            case Function_type.NOISE_FILTER:
                self.__noise_filter(function.args)
                return None
            case Function_type.USEFUL_SIGNAL:
                self.__useful_signal(function.args)
                return None
            case Function_type.TRIM:
                self.__trim(function.args)
                return None
            case Function_type.XYZ_DIAGRAM:
                return self.__xyz_diagram(function.args)
            case Function_type.XY_DIAGRAM:
                return self.__xy_diagram(function.args)

    @staticmethod
    def copy(obj: 'Audio_track', params: list[Any]) -> list['Audio_track']:
        pass

    @staticmethod
    def from_wav(track: UploadFile, to_separate_track: bool = False) -> list['Audio_track']:
        sample_rate, tracks = scipy.io.wavfile.read(track)

        if to_separate_track and len(tracks) > 1:
            return [Audio_track(track, sample_rate) for track in tracks]
        elif len(tracks) != 1:
            track = numpy.mean(tracks, axis=0)
            return [Audio_track(track, sample_rate),]
        else:
            return [Audio_track(tracks, sample_rate),]

        return scipy.io.wavfile.read(track.file)