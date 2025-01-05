from enum import Enum
from functions.data_classes import Pipeline, Function_call, Time # Track_characteristic,
from fastapi import UploadFile
from io import BytesIO
import scipy
import numpy
from typing import Any
from noisereduce import reduce_noise
import zipfile
import copy
from matplotlib import pyplot as plt
# from functions.utils import pseudo_zip_result


def make_pipeline(track: UploadFile, pipeline: Pipeline, to_separate_track: bool) -> BytesIO:
    tracks: list[Audio_track] | Audio_track = Audio_track.from_wav(track, to_separate_track)
    images: list[BytesIO] = [] # has duplication names
    for i in range(len(pipeline.pipeline)):
        image = Audio_track.use_function(tracks, pipeline.pipeline[i], i)
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
    def use_function(tracks: list['Audio_track'], function: Function_call, function_num: int) -> BytesIO | None:
        return Audio_track.use_function_lambda(tracks, function, function_num)

    @staticmethod
    def set_use_function(is_debug: bool) -> None:
        if is_debug:
            Audio_track.use_function_lambda = Audio_track.use_function_debug
        else:
            Audio_track.use_function_lambda = Audio_track.use_function_release

    @staticmethod
    def get_check_track_for_function_call(tracks: list['Audio_track'], function: Function_call) -> tuple['Audio_track', int]:
        '''
        returns track that was asked by function and last coordinate in tracks (to use in functions that multiply tracks)
        '''
        track_list = tracks

        # decompose track list from list of tracks and lists
        # tracks = [track0, [track1_1, track1_2]]
        # result track_list = [track1_1, track1_2] and check of fucntion call
        for i in range(len(function.track) - 1):
            if i >= len(track_list):
                raise ValueError("Track id is out of range")
            track_list = track_list[function.track[i]]

        track_id = function.track[-1]
        if track_id >= len(track_list):
            raise ValueError("Track id is out of range")

        return track_list[track_id], track_id

    @staticmethod
    def use_function_release(tracks: list['Audio_track'], function: Function_call, unused: int) -> BytesIO | None:
        track, track_id = Audio_track.get_check_track_for_function_call(tracks, function)

        if function.id == Function_type.COPY:
            tracks[track_id] = Audio_track.__copy(track, function.args)
            return None
        else:
            return track.__function_call(function)

    @staticmethod
    def use_function_debug(tracks: list['Audio_track'], function: Function_call, function_num: int) -> BytesIO | None:
        # overhead of double check in debug and in release functions - don't use in production
        _, track_id = Audio_track.get_check_track_for_function_call(tracks, function)

        copy_of_track = copy.deepcopy(tracks[track_id])

        result: BytesIO | None = Audio_track.use_function_release(tracks, function, function_num)
        if result is BytesIO:
            return result

        # make plot
        try:
            y1 = copy_of_track.time_domain_track
            y2 = tracks[track_id].time_domain_track

            # Create time axes for plotting
            time = numpy.linspace(0, len(y1) / copy_of_track.sample_rate, len(y1))

            # Plot the waveforms
            plt.figure(figsize=(15, 6))

            plt.subplot(2, 1, 1)
            plt.plot(time, y1, color='blue')
            plt.title('Waveform of Track 1')
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')

            plt.subplot(2, 1, 2)
            plt.plot(time, y2, color='green')
            plt.title('Waveform of Track 2')
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')

            plt.tight_layout()

            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            buffer.name = f"plot{function_num}.png"
            plt.close()
            return buffer

        except Exception as e:
            print(f"An error occurred: {e}")

        return None

    # -------------------------------------------------------------

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
        # ora = scipy.signal.butter(N=30, Wn=pivotal_frequency, fs=self.sample_rate, btype='lowpass', output='sos')
        # self.time_domain_track = scipy.signal.sosfilt(self.time_domain_track, ora)
        # return

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

    @staticmethod
    def debug_tracks_to_plot(tracks: list['Audio_track']) -> BytesIO:
        pass

    @staticmethod
    def debug_track_to_plot(track: 'Audio_track') -> BytesIO:
        pass