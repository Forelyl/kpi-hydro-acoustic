from enum import Enum
from server.functions.data_classes import Pipeline, Function_call, Time
from fastapi import UploadFile
from io import BytesIO
import scipy
import numpy
from typing import Any
from noisereduce import reduce_noise
import zipfile
import copy
from matplotlib import pyplot as plt
from fastapi import HTTPException, status

import math
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
    LOW_PASS                             = 0
    HIGH_PASS                            = 1
    BAND_PASS                            = 2
    NOTCH_FILTER                         = 3
    GAIN                                 = 4
    LEVEL                                = 5
    NOISE_FILTER                         = 6
    USEFUL_SIGNAL                        = 7

    TRIM                                 = 8

    XYZ_DIAGRAM_TIME_FREQUENCY_AMPLITUDE = 9
    XY_DIAGRAM_FREQUENCY_2_AMPLITUDE     = 10
    COPY                                 = 12


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
    def use_function_release(tracks: list['Audio_track'], function: Function_call, function_num: int) -> BytesIO | None:
        track, track_id = Audio_track.get_check_track_for_function_call(tracks, function)

        if function.f_id == Function_type.COPY:
            tracks[track_id] = Audio_track.__copy(track, function.args)
            return None
        else:
            return track.function_call(function, function_num)

    @staticmethod
    def use_function_debug(tracks: list['Audio_track'], function: Function_call, function_num: int) -> BytesIO | None:
        # overhead of double check in debug and in release functions - don't use in production
        _, track_id = Audio_track.get_check_track_for_function_call(tracks, function)

        copy_of_track = copy.deepcopy(tracks[track_id])

        result: BytesIO | None = Audio_track.use_function_release(tracks, function, function_num)
        if type(result) is BytesIO:
            return result

        # =================
        # Compare two audio tracks and plot their spectrograms.
        # =================

        # Perform FFT on the audio data
        n1 = len(copy_of_track.time_domain_track)  # Number of samples
        win1 = numpy.hamming(n1)
        frequencies1 = numpy.fft.fftfreq(n1, 1 / copy_of_track.sample_rate)     # Frequency bins
        spectrum1    = numpy.fft.rfft(copy_of_track.time_domain_track * win1)   # Perform FFT

        n2 = len(tracks[track_id].time_domain_track)  # Number of samples
        win2 = numpy.hamming(n2)
        frequencies2 = numpy.fft.fftfreq(n2, 1 / tracks[track_id].sample_rate)   # Frequency bins
        spectrum2    = numpy.fft.rfft(tracks[track_id].time_domain_track * win2) # Perform FFT

        # Get the magnitude of the spectrum and the positive frequencies
        spectrum_magnitude1   = numpy.abs(spectrum1)
        positive_frequencies1 = frequencies1[:n1 //  2]
        positive_magnitude1   = spectrum_magnitude1[:n1 // 2] / numpy.amax(spectrum_magnitude1)
        db_magnitude1 = 20 * numpy.log10(positive_magnitude1)

        spectrum_magnitude2   = numpy.abs(spectrum2)
        positive_frequencies2 = frequencies2[:n2 // 2]
        positive_magnitude2   = spectrum_magnitude2[:n2 // 2] / numpy.amax(spectrum_magnitude2)
        db_magnitude2 = 20 * numpy.log10(positive_magnitude2)

        # Plot the spectrum
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

        ax1.plot(positive_frequencies1, db_magnitude1, label='Spectrum', color='blue', linewidth=0.5)
        ax1.set_title('Original')
        ax1.set_xlabel('Frequency (Hz)')
        ax1.set_ylabel('Magnitude')
        ax1.legend()

        ax2.plot(positive_frequencies2, db_magnitude2,  label='Spectrum', color='red', linewidth=0.5)
        ax2.set_title('Processed')
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('Magnitude')
        ax2.legend()

        plt.tight_layout()

        # Save the plot to a file
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        buffer.name = f"comparison_spectrogram{function_num}.png"
        plt.close()
        return buffer

    # -------------------------------------------------------------

    def function_call(self, function: Function_call, function_num: int) -> BytesIO | None:
        match function.f_id:
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
            case Function_type.XYZ_DIAGRAM_TIME_FREQUENCY_AMPLITUDE:
                return self.__xyz_diagram_tfa(function.args, function_num)
            case Function_type.XY_DIAGRAM_FREQUENCY_2_AMPLITUDE:
                return self.__xy_diagram_fa(function.args, function_num)
            case Function_type.COPY:
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal error, incorrect copy route")
                return None

    @staticmethod
    def __copy(obj: 'Audio_track', params: list[Any]) -> list['Audio_track']:
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

    def __low_pass(self, args: list[Any]):
        pivotal_frequency: float = args[0] # Hz

        b_low, a_low = scipy.signal.butter(N=3, Wn=pivotal_frequency, btype="lowpass", fs=self.sample_rate)
        self.time_domain_track = scipy.signal.filtfilt(b_low, a_low, self.time_domain_track)

    def __high_pass(self, args: list[Any]):
        pivotal_frequency: float = args[0] # Hz

        b_low, a_low = scipy.signal.butter(N=3, Wn=pivotal_frequency, btype="highpass", fs=self.sample_rate)
        self.time_domain_track = scipy.signal.filtfilt(b_low, a_low, self.time_domain_track)
        return

    def __band_pass(self, args: list[Any]):
        in_pivotal_frequency_left:  float = args[0] # Hz
        in_pivotal_frequency_right: float = args[1] # Hz
        b_low, a_low = scipy.signal.butter(N=3, Wn=[in_pivotal_frequency_left, in_pivotal_frequency_right], btype="bandpass", fs=self.sample_rate)
        self.time_domain_track = scipy.signal.filtfilt(b_low, a_low, self.time_domain_track)

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
        self.time_domain_track = (self.time_domain_track * linear_gain).astype(numpy.int16)

    def __level(self, args: list[Any]):
        level: float = args[0] / 100 # %
        self.time_domain_track = (self.time_domain_track * level).astype(numpy.int16)

    def __noise_filter(self, args: list[Any]):
        self.time_domain_track = reduce_noise(y=self.time_domain_track, sr=self.sample_rate)

    def __useful_signal(self, args: list[Any]):
        level: float = args[0] # dB
        linear_gain = 10 ** (level / 20)
        useful_signal = reduce_noise(y=self.time_domain_track, sr=self.sample_rate)
        self.time_domain_track += (useful_signal * linear_gain).astype(numpy.int16)

    def __trim(self, args: list[Any]):
        start: Time = args[0] # min, seconds
        end:   Time = args[1] # min, seconds
        start: int  = start.minutes * 60 + start.seconds
        end:   int  = end.minutes * 60 + end.seconds

        # check start <= end
        amount_of_samples = self.time_domain_track.shape[0]
        length = amount_of_samples / self.sample_rate # seconds

        # ---------------

        if start > end:
            raise ValueError(f'Start time is greater than end time: {start} > {end}')

        if start > length:
            raise ValueError(f'Start time is greater than track length: {start} > {length}')

        if start < 0:
            start: int = 0

        if end > length:
            end = length

        # ---------------

        self.time_domain_track = self.time_domain_track[math.floor(start * self.sample_rate):math.floor(end * self.sample_rate)]

    def __xyz_diagram_tfa(self, args: list[Any], function_num: int) -> BytesIO:
        # Perform Short-Time Fourier Transform (STFT) for time-frequency analysis
        segment_length = 1024  # Number of samples per segment
        overlap = segment_length // 2  # 50% overlap
        window = numpy.hamming(segment_length)

        # Compute STFT
        freqs, times, Zxx = scipy.signal.stft(
            self.time_domain_track,
            fs=self.sample_rate,
            window=window,
            nperseg=segment_length,
            noverlap=overlap,
            boundary=None
        )

        # Compute magnitude and convert to dB scale
        magnitude = numpy.abs(Zxx)
        magnitude_db = 20 * numpy.log10(magnitude + numpy.finfo(float).eps)

        # Plotting the heatmap spectrogram
        fig, ax = plt.subplots(figsize=(20, 10))

        # Create the heatmap
        cax = ax.pcolormesh(times, freqs, magnitude_db, cmap='viridis', shading='gouraud')

        # Customize the plot
        ax.set_title(f'Heatmap Spectrogram functioncall-{function_num + 1}')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Frequency (Hz)')

        # Add a color bar to indicate amplitude
        fig.colorbar(cax, ax=ax, label='Amplitude (dB)')

        # Save the plot to a buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        buffer.name = f"Heatmap_Spectrogram_functioncall{function_num + 1}.png"
        plt.close()

        return buffer

    def __xy_diagram_fa(self, args: list[Any], function_num: int) -> BytesIO:
        # Perform FFT on the audio data
        n = len(self.time_domain_track)  # Number of samples
        win = numpy.hamming(n)
        frequencies = numpy.fft.fftfreq(n, 1 / self.sample_rate)     # Frequency bins
        spectrum    = numpy.fft.rfft(self.time_domain_track * win)   # Perform FFT

        # Get the magnitude of the spectrum and the positive frequencies
        spectrum_magnitude   = numpy.abs(spectrum)
        positive_frequencies = frequencies[:n //  2]
        positive_magnitude   = spectrum_magnitude[:n // 2] / numpy.amax(spectrum_magnitude)
        db_magnitude = 20 * numpy.log10(positive_magnitude)

        # Plot the spectrum
        plt.figure(figsize=(20, 10))

        plt.plot(positive_frequencies, db_magnitude, label='Spectrum', color='blue', linewidth=0.5)
        plt.title(f'2D Signal spectogram functioncall-{function_num + 1}')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude (dB)')
        plt.legend()

        plt.tight_layout()

        # Save the plot to a file
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        buffer.name = f"2D_Signal_spectogram_functioncall{function_num + 1}.png"
        plt.close()
        return buffer
