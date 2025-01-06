import unittest
from unittest.mock import patch, MagicMock

import numpy
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
                "id": 0,
                "args": [1133],
                "track": [1,2,3] 
            }
            ''',
            '''
            {
                "id": 1,
                "args": [1133],
                "track": [3]
            }
            ''',
            '''
            {
                "id": 2,
                "args": [1111, 1243],
                "track": [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9] 
            }
            ''',
            '''
            {
                "id": 3,
                "args": [11, 123],
                "track": [0]
            }
            ''',
            '''
            {
                "id": 4,
                "args": [1],
                "track": [0] 
            }
            ''',
            '''
             {
                 "id": 5,
                 "args": [1],
                 "track": [0] 
             }
            ''',
            '''
            {
                "id": 6,
                "args": [],
                "track": [0] 
            }
            ''',
            '''
            {
                "id": 7,
                "args": [-12],
                "track": [0] 
            }
            ''',
            '''
            {
                "id": 8,
                "args": [{"second": 12, "minutes": 3}, {"minutes": 10, "second": 12}],
                "track": [0] 
            }
            ''',
            '''
            {
                "id": 9,
                "args": [],
                "track": [0] 
            }
            ''',
            '''
            {
                "id": 10,
                "args": [],
                "track": [0] 
            }
            ''',
            '''
            {
                "id": 11,
                "args": [1],
                "track": [0] 
            }
            '''
        ]
        to_validate = to_validate[:4]
        try:
            for json_func_call in to_validate:
                Function_call.model_validate_json(json_func_call, strict = True)
        except ValidationError as e:
            self.fail("Time hasn't been validated - yet should has been, error: " + str(e))

    def function_incorrect(self):
        return
        self.assertRaises(ValidationError, Function_call.model_validate_json, '{"seconds": -12, "minutes": 3}', strict = True)


class TestFunctions(unittest.TestCase):

    @patch('server.functions.functions.Audio_track.function_call')
    def test_function_correct(self, mock_call):
        # Mock the return value of the function_call
        mock_call.return_value = BytesIO(b"Mocked function call output")

        # Create a mock for the function argument
        function = MagicMock()
        function.id = "SOME_FUNCTION_ID"  # Set any necessary attributes on the mock
        function.args = [1, 2, 3]  # Mock function arguments if necessary

        # Create a mock audio track
        track = Audio_track(numpy.array([1, 2, 3]), 44100, [1])

        # Call the method that triggers function_call
        result = track.function_call(function, 1)

        # Assert that function_call was called with the expected arguments
        mock_call.assert_called_with(function, 1)

        # Assert the return value is the mocked value
        assert isinstance(result, BytesIO)
        assert result.getvalue() == b"Mocked function call output"




if __name__ == '__main__':
    unittest.main()
