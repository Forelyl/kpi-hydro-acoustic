from enum import Enum
from functions.data_classes import Pipeline, Function_call, Track_characteristic, Time
from fastapi import UploadFile
from io import BytesIO
import scipy
import numpy
from typing import Any
from noisereduce import reduce_noise
import zipfile
from functions.utils import pseudo_zip_result
from matplotlib import pyplot as plt

def make_pipeline(track: UploadFile, pipeline: Pipeline, to_separate_track: bool) -> BytesIO:
    tracks: list[Audio_track] | Audio_track = Audio_track.from_wav(track, to_separate_track)
    images: list[BytesIO] = [] # has duplication names
    print(type(tracks[0].time_domain_track[0]))
    for function in pipeline.pipeline: # TODO: use async to make it faster
        image = Audio_track.use_function(tracks, function)
        if image is not None:
            images.append(image)

    for track in tracks:
        track.prepare_to_writing()

    # result audio and images
    byte_tracks = [
        BytesIO() for _ in tracks  # Create a new BytesIO object for each track
    ]


    # Write WAV data to each BytesIO object
    for byte_track, track in zip(byte_tracks, tracks):
        scipy.io.wavfile.write(byte_track, track.sample_rate, track.time_domain_track)
        byte_track.name = f"{track.get_name()}.wav"

    # full zip file
    zip_file = BytesIO()
    zip_file.name = "result.zip"
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zip_writer:

        for byte_track in byte_tracks:
            zip_writer.writestr(byte_track.name, byte_track.read())

        for image in images:
            zip_writer.writestr(image.name, image.read())

    zip_file.seek(0)

    return zip_file


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
    def __init__(self, track: numpy.ndarray | None = None, sample_rate: int | None = None, name: list[int] | None = None):
        if track is None or sample_rate is None or name is None:
            if track is not None or sample_rate is not None or name is not None:
                raise ValueError("If you want to create a track, you need to pass all or non the arguments")
            return

        self.time_domain_track = track
        self.sample_rate       = sample_rate
        self.track_name        = name

    def get_name(self) -> str:
        return ".".join(map(str, self.track_name))

    def prepare_to_writing(self):
        self.time_domain_track = self.time_domain_track.astype(numpy.int16)

    @staticmethod
    def use_function(tracks: list['Audio_track'], function: Function_call) -> BytesIO | None:
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
        n = params[0]
        copies: list[Audio_track] = []
        time_domain = obj.time_domain_track

        copies.append(obj)

        for _ in range(n - 1):
            temp = Audio_track()
            temp.time_domain_track = time_domain.copy()
            temp.sample_rate = obj.sample_rate
            copies.append(temp)

        for i in range(len(copies)):
            copies[i].track_name.append(i)

        return copies

    @staticmethod
    def from_wav(track: UploadFile, to_separate_track: bool = False) -> list['Audio_track']:
        sample_rate, tracks = scipy.io.wavfile.read(track.file)
        if to_separate_track and len(tracks.shape) > 1:
            return [Audio_track(tracks[:, i], sample_rate, [i, ]) for i in range(tracks.shape[1])]
        elif len(tracks.shape) != 1:
            track = numpy.mean(tracks, axis=1)
            return [Audio_track(track, sample_rate, [1,]),]
        else:
            return [Audio_track(tracks, sample_rate, [1,]),]

        return scipy.io.wavfile.read(track.file)

    @staticmethod
    def __all_pass(input_signal, cutoff_frequency, sample_rate):
        dn_1 = 0
        allpass_output = numpy.zeros_like(input_signal)
        for n in range(input_signal.shape[0]):
            tan = numpy.tan(numpy.pi * cutoff_frequency / sample_rate)
            a1 = (tan - 1) / (tan + 1)

            allpass_output[n] = a1 * input_signal[n] + dn_1

            dn_1 = input_signal[n] - a1 * allpass_output[n]

        return allpass_output

    def __low_pass(self, args: list[Any]):
        pivotal_frequency: float = args[0] # Hz
        ora = numpy.signal.butter(N=1, Wn=pivotal_frequency, fs=self.sample_rate, btype='lowpass', output='sos')
        self.time_domain_track = numpy.signal.sosfilt(self.time_domain_track, ora)
        return

        allpass_res = self.__all_pass(self.time_domain_track, pivotal_frequency, self.sample_rate)
        self.time_domain_track = self.time_domain_track + allpass_res

        self.time_domain_track = self.time_domain_track.astype(numpy.float64)
        self.time_domain_track *= 0.5

    def __high_pass(self, args: list[Any]):
        pivotal_frequency: float = args[0] # Hz

        allpass_res = self.__all_pass(self.time_domain_track, pivotal_frequency, self.sample_rate)
        self.time_domain_track = self.time_domain_track - allpass_res

        self.time_domain_track = self.time_domain_track.astype(numpy.float64)
        self.time_domain_track *= 0.5
        return

    def __band_pass(self, args: list[Any]):
        # https://thewolfsound.com/allpass-based-bandstop-and-bandpass-filters/
        in_pivotal_frequency_left:  float = args[0] # Hz
        in_pivotal_frequency_right: float = args[1] # Hz
        self.__high_pass([in_pivotal_frequency_left])
        self.__low_pass([in_pivotal_frequency_right])

    def __notch_filter(self, args: list[Any]):
        out_pivotal_frequency_left:  float = args[0] # Hz
        out_pivotal_frequency_right: float = args[1] # Hz

        middle = (out_pivotal_frequency_left + out_pivotal_frequency_right) / 2
        quality_factor = max(1.0, middle / (out_pivotal_frequency_right - out_pivotal_frequency_left))

        b, a = scipy.signal.iirnotch(w0=middle, Q=quality_factor, fs=self.sample_rate)
        self.time_domain_track = scipy.signal.lfilter(b, a, self.time_domain_track)

    def __gain(self, args: list[Any]):
        level: float = args[0] # dB
        linear_gain = 10 ** (level / 20)
        self.time_domain_track *= linear_gain

    def __level(self, args: list[Any]):
        level: float = args[0] # %
        self.time_domain_track *= level / 100

    def __noise_filter(self, args: list[Any]):
        self.time_domain_track = reduce_noise(y=self.time_domain_track, sr=self.sample_rate)

    def __useful_signal(self, args: list[Any]):
        level: float = args[0] # dB
        linear_gain = 10 ** (level / 20)
        useful_signal = reduce_noise(y=self.time_domain_track, sr=self.sample_rate)
        self.time_domain_track += useful_signal * linear_gain

    def __trim(self, args: list[Any]):
        start: Time = args[0] # min, seconds
        end:   Time = args[1] # min, seconds
        start = start.minutes * 60 + start.seconds
        end   = end.minutes * 60 + end.seconds

        # check start <= end
        amount_of_samples = self.time_domain_track.shape[0]
        length = amount_of_samples * self.sample_rate # seconds

        # ---------------

        if start > end:
            raise ValueError(f'Start time is greater than end time: {start} > {end}')

        if start > length:
            raise ValueError(f'Start time is greater than track length: {start} > {length}')

        if start < 0:
            start = 0

        if end > length:
            end = length

        # ---------------

        self.time_domain_track = self.time_domain_track[int(start * self.sample_rate):int(end * self.sample_rate)]

    def __xyz_diagram(self, args: list[Any]) -> BytesIO:
        pass

    def __xy_diagram(self, args: list[Any]) -> BytesIO:
        pass