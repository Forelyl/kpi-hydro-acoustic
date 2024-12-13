from functions.data_classes import Pipeline # , Function_call, Track_characteristic, Time
from fastapi import UploadFile
from io import BytesIO
from functions.utils import pseudo_zip_result
import scipy
import numpy

def make_pipeline(track: UploadFile, pipeline: Pipeline, to_separate_track: bool) -> BytesIO:

    return pseudo_zip_result()


class Audio_track:
    def __init__(self, track: numpy.ndarray, sample_rate: int):
        self.frequency_domain_track = scipy.fft.rfft(track) # maybe incorrect

    def use_functions(self, function: Function_call):
        pass

    def some_funct(): pass

    @staticmethod
    def from_wav(track: UploadFile, to_separate_track: bool = False):
        sample_rate, tracks = scipy.io.wavfile.read(track)

        if to_separate_track and len(tracks) > 1:
            return [Audio_track(track, sample_rate) for track in tracks]
        elif len(tracks) != 1:
            track = numpy.mean(tracks, axis=0)
            return Audio_track(track, sample_rate)
        else:
            return Audio_track(tracks, sample_rate)

        return scipy.io.wavfile.read(track.file)