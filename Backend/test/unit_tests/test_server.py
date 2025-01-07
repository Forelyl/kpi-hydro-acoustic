import unittest
from unittest.mock import patch

import numpy
import numpy as np
from pydantic import ValidationError
from server.functions.data_classes import *
from io import BytesIO

from server.functions.functions import Audio_track


class TestDataclasses(unittest.TestCase):
    def test_time_correct(self):
        try:
            Time.model_validate_json('{"seconds": 12, "minutes": 3}', strict = True)
            Time.model_validate_json('{"seconds": 12, "minutes": 0}', strict = True)
            Time.model_validate_json('{"seconds": 0, "minutes": 123}', strict = True)
            Time.model_validate_json('{"minutes": 3, "seconds": 12}', strict = True)
        except ValidationError as e:
            self.fail("Time hasn't been validated - yet should has been, error: " + str(e))

    def test_time_incorrect(self):
        self.assertRaises(ValidationError, Time.model_validate_json, '{"seconds": -12, "minutes": 3}', strict = True)
        self.assertRaises(ValidationError, Time.model_validate_json, '{"seconds": 12, "minutes": -3}', strict = True)
        self.assertRaises(ValidationError, Time.model_validate_json, '{"seconds": -12, "minutes": -3}', strict = True)
        self.assertRaises(ValidationError, Time.model_validate_json, '{"seconds": sdf, "minutes": 3}', strict = True)
        self.assertRaises(ValidationError, Time.model_validate_json, '{"seconds": 56, "minutes": sdf}', strict = True)
        self.assertRaises(ValidationError, Time.model_validate_json, '{"seconds": 60, "minutes": 0}', strict = True)
        self.assertRaises(ValidationError, Time.model_validate_json, '{"errr": 2, "minutes": 0}', strict = True)
        self.assertRaises(ValidationError, Time.model_validate_json, '{"seconds": 60, "not_correct": 0}', strict = True)

    def test_function_correct(self):
        to_validate: list[str] = [
            '''
            {
                "f_id": 0,
                "args": [1133],
                "track": [1,2,3] 
            }
            ''',
            '''
            {
                "f_id": 1,
                "args": [1133],
                "track": [3]
            }
            ''',
            '''
            {
                "f_id": 2,
                "args": [1111, 1243],
                "track": [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9] 
            }
            ''',
            '''
            {
                "f_id": 3,
                "args": [11, 123],
                "track": [1]
            }
            ''',
            '''
            {
                "f_id": 4,
                "args": [1],
                "track": [2] 
            }
            ''',
            '''
             {
                 "f_id": 5,
                 "args": [1],
                 "track": [1] 
             }
            ''',
            '''
            {
                "f_id": 6,
                "args": [],
                "track": [1] 
            }
            ''',
            '''
            {
                "f_id": 7,
                "args": [-12],
                "track": [1] 
            }
            ''',
            '''
            {
                "f_id": 8,
                "args": [{"seconds": 12, "minutes": 3}, {"minutes": 10, "seconds": 12}],
                "track": [1] 
            }
            ''',
            '''
            {
                "f_id": 9,
                "args": [],
                "track": [1] 
            }
            ''',
            '''
            {
                "f_id": 10,
                "args": [],
                "track": [1] 
            }
            ''',
            '''
            {
                "f_id": 11,
                "args": [1],
                "track": [1] 
            }
            '''
        ]
        to_validate = to_validate[:4]
        try:
            for json_func_call in to_validate:
                Function_call.model_validate_json(json_func_call, strict = True)
        except ValidationError as e:
            self.fail("Time hasn't been validated - yet should has been, error: " + str(e))

    def test_function_incorrect(self):
        self.assertRaises(ValidationError, Function_call.model_validate_json,             '''
            {
                "f_id": 13,
                "args": [1],
                "track": [1] 
            }
            ''', strict = True)
        self.assertRaises(ValidationError, Function_call.model_validate_json,             '''
            {
                "f_id": -1,
                "args": [1],
                "track": [1] 
            }
            ''', strict = True)
        self.assertRaises(ValidationError, Function_call.model_validate_json,             '''
            {
                "f_id": 1,
                "args": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                "track": [1] 
            }
            ''', strict = True)
        self.assertRaises(ValidationError, Function_call.model_validate_json,             '''
            {
                "f_id": 1,
                "args": [],
                "track": [1] 
            }
            ''', strict = True)
        self.assertRaises(ValidationError, Function_call.model_validate_json,             '''
            {
                "f_id": 1,
                "args": [1],
                "track": [-1] 
            }
            ''', strict = True)

        self.assertRaises(ValidationError, Function_call.model_validate_json,             '''
            {
                "f_id": 13,
                "args": [1],
                "track": [] 
            }
            ''', strict = True)

class TestFunctions(unittest.TestCase):
    #server.functions.functions.Audio_track.

    def setUp(self):
        self.functions_to_call: list[Function_call] = [
            Function_call(**{"f_id": 0, "track": [1], "args": [1,]}),
            Function_call(**{"f_id": 1, "track": [1], "args": [1,]}),
            Function_call(**{"f_id": 2, "track": [1], "args": [1, 2]}),
            Function_call(**{"f_id": 3, "track": [1], "args": [1, 2]}),
            Function_call(**{"f_id": 4, "track": [1], "args": [1,]}),
            Function_call(**{"f_id": 5, "track": [1], "args": [1,]}),
            Function_call(**{"f_id": 6, "track": [1], "args": []}),
            Function_call(**{"f_id": 7, "track": [1], "args": [1,]}),
            Function_call(**{"f_id": 8, "track": [1], "args": [
                {"seconds": 1, "minutes": 0}, {"seconds": 2, "minutes": 0}
            ]}),
            Function_call(**{"f_id": 9, "track": [1], "args": []}),
            Function_call(**{"f_id": 10, "track": [1], "args": []}),
            Function_call(**{"f_id": 11, "track": [1], "args": [1,]}),
        ]

    @patch.object(Audio_track, '_Audio_track__copy')
    @patch.object(Audio_track, '_Audio_track__xy_diagram_fa')
    @patch.object(Audio_track, '_Audio_track__xyz_diagram_tfa')
    @patch.object(Audio_track, '_Audio_track__trim')
    @patch.object(Audio_track, '_Audio_track__useful_signal')
    @patch.object(Audio_track, '_Audio_track__noise_filter')
    @patch.object(Audio_track, '_Audio_track__level')
    @patch.object(Audio_track, '_Audio_track__gain')
    @patch.object(Audio_track, '_Audio_track__notch_filter')
    @patch.object(Audio_track, '_Audio_track__band_pass')
    @patch.object(Audio_track, '_Audio_track__high_pass')
    @patch.object(Audio_track, '_Audio_track__low_pass')

    def test_function_call_calling(self, function_call0, function_call1, function_call2, function_call3, function_call4, function_call5,
                                   function_call6, function_call7, function_call8, function_call9, function_call10, function_call11):
        function_calls = [
            function_call0, function_call1, function_call2,
            function_call3, function_call4, function_call5,
            function_call6, function_call7, function_call8,
            function_call9, function_call10, function_call11
        ]

        for i in range(len(function_calls)):
            file_name = f"File for usage of function number - {i}"
            file_contents = f"This is the contents of file {i}."
            file = StringIO(file_name)
            file.write(file_contents)
            file.seek(0)
            bytes_read = BytesIO(bytes(file.read().encode('utf-8')))
            function_calls[i].return_value = bytes_read
        samplerate = 44100
        duration = 5

        # Calculate the number of samples
        num_samples = int(samplerate * duration)

        # Generate random data
        data = np.random.randint(-32768, 32767, size=num_samples, dtype=np.int16)
        track: list[Audio_track] = [Audio_track(data, 44100, [1])]

        for i in range(0, len(function_calls)):
            if i == 11: # skip copy - other route for calling
                continue
            Audio_track.use_function_release(track, self.functions_to_call[i], i)
            if i in [9, 10]: # special call for diagrams
                function_calls[i].assert_called_with(self.functions_to_call[i].args, i)
            else:
                function_calls[i].assert_called_with(self.functions_to_call[i].args)

    @patch("server.functions.functions.Audio_track.function_call")
    def test_function_call(self, function_call):

        function_call.return_value = None
        samplerate = 44100
        duration = 5

        # Calculate the number of samples
        num_samples = int(samplerate * duration)

        # Generate random data
        data = np.random.randint(-32768, 32767, size=num_samples, dtype=np.int16)
        track: list[Audio_track] = [Audio_track(data, 44100, [1])]

        Audio_track.use_function_release(track, self.functions_to_call[0], 0)
        function_call.assert_called_with(Function_call(**{"f_id": 0, "track": [1], "args": [1,]}), 0)

class TestCallFunctions(unittest.TestCase):

    def setUp(self):
        self.data_change_functions: list[Function_call] = [
            Function_call(**{"f_id": 0, "track": [1], "args": [1, ]}),
            Function_call(**{"f_id": 1, "track": [1], "args": [1, ]}),
            Function_call(**{"f_id": 2, "track": [1], "args": [1, 2]}),
            Function_call(**{"f_id": 3, "track": [1], "args": [1, 2]}),
            Function_call(**{"f_id": 4, "track": [1], "args": [1, ]}),
            Function_call(**{"f_id": 5, "track": [1], "args": [1, ]}),
            Function_call(**{"f_id": 6, "track": [1], "args": []}),
            Function_call(**{"f_id": 7, "track": [1], "args": [1, ]})
        ]

        self.graphical_functions_to_check: list[Function_call] = [
            Function_call(**{"f_id": 9, "track": [1], "args": []}),
            Function_call(**{"f_id": 10, "track": [1], "args": []})
        ]

        self.trim_func = Function_call(**{
            "f_id": 8, 
            "track": [1], 
            "args": [{"seconds": 1, "minutes": 0}, {"seconds": 2, "minutes": 0}]
        })


    def test_data_change_full_functions(self):
        samplerate = 44100
        duration = 5

        # Calculate the number of samples
        num_samples = int(samplerate * duration)
        data = np.random.randint(-32768, 32767, size=num_samples, dtype=np.int16)
        tracks: list[Audio_track] = [Audio_track(data, 44100, [1]),]
        old_data = copy.copy(data)

        for x in self.data_change_functions:
            use_tracks = copy.deepcopy(tracks)
            Audio_track.use_function_release(use_tracks, x, random.randint(0, 10))
            result_track = old_data - use_tracks[0].time_domain_track
            zero_track = numpy.zeros(len(result_track))
            self.assertFalse(numpy.array_equal(result_track, zero_track))


    def test_data_size_change_functions(self):
        samplerate = 44100
        duration = 5 # range [1, 2] is been cut

        # Calculate the number of samples
        num_samples = int(samplerate * duration)
        data = np.random.randint(-32768, 32767, size=num_samples, dtype=np.int16)
        tracks: list[Audio_track] = [Audio_track(data, 44100, [1]),]
        old_data = copy.copy(data)

        Audio_track.use_function_release(tracks, self.trim_func, random.randint(0, 10))

        # compare length
        self.assertGreater(len(old_data), len(tracks[0].time_domain_track))


    def test_image_generate_functions(self):

        samplerate = 44100
        duration = 5

        possible_results = [
            f"Heatmap_Spectrogram_functioncall1.png",
            f"2D_Signal_spectogram_functioncall1.png"
        ]

        # Calculate the number of samples
        num_samples = int(samplerate * duration)
        data = np.random.randint(-32768, 32767, size=num_samples, dtype=np.int16)
        track: list[Audio_track] = [Audio_track(data, 44100, [1])]

        for i in range(0, len(self.graphical_functions_to_check)):
            result = Audio_track.use_function_release(track, self.graphical_functions_to_check[i], 0)
            self.assertEqual(result.name, possible_results[i])
            self.assertTrue(result.getvalue().startswith(b'\x89PNG'))


class TestGlobalCheck(unittest.TestCase):

    class FakeUploadFile:
        def __init__(self, filename: str, content: bytes):
            self.filename = filename
            self.file = BytesIO(content)

        async def read(self) -> bytes:
            """Simulates the async read method of UploadFile."""
            self.file.seek(0)
            return self.file.read()

        def write(self, data: bytes):
            """Allows writing to the file for completeness."""
            self.file.write(data)

        def close(self):
            """Simulates closing the file."""
            self.file.close()

    class FakePipeline:
        def __init__(self):
            self.pipeline: list = [None,]

    @patch('server.functions.functions.Audio_track.use_function')
    def test_global_pipeline_check(self, stub_use_function):
        stub_use_function.return_value = None
        with open( '../test-data/test_file.wav', 'rb') as test_file:
            wav_file_as_bytes = test_file.read()

        #
        pseudo_upload = self.FakeUploadFile('test_file.wav', wav_file_as_bytes)
        pseudo_pipeline = self.FakePipeline()
        result: BytesIO = make_pipeline(pseudo_upload, pseudo_pipeline, True)

        self.assertEqual(result.name, "result.zip")
        self.assertTrue(result.getvalue().startswith(b'PK\x03\x04'))


if __name__ == '__main__':
    unittest.main()
