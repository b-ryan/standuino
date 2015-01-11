import unittest
import standuino.arduino as ard
import json


class TestArduino(unittest.TestCase):
    def setUp(self):
        self.message = {
            "distance_cm": 200,
        }

    def tearDown(self):
        pass

    def test_parse_ok(self):
        self.assertIsNotNone(ard.parse_and_validate(json.dumps(self.message)))

    def test_parse_invalid_json(self):
        s = json.dumps(self.message)[:-1]
        self.assertRaises(ard.ValidationException, ard.parse_and_validate, s)

    def test_parse_invalid_key(self):
        s = json.dumps({"x": 1})
        self.assertRaises(ard.ValidationException, ard.parse_and_validate, s)
