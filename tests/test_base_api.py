import unittest
from unittest.mock import MagicMock, patch

import requests

from src.base_api import OpenSkyAdapter


class TestOpenSkyAdapter(unittest.TestCase):

    def setUp(self):
        self.adapter = OpenSkyAdapter()

    @patch("requests.get")
    def test_get_country_bounds_success(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = [{"boundingbox": ["50.0", "60.0", "10.0", "20.0"]}]
        mock_get.return_value = mock_resp

        result = self.adapter.get_country_bounds("Testland")
        self.assertEqual(result, {"south": 50.0, "north": 60.0, "west": 10.0, "east": 20.0})

    @patch("requests.get")
    def test_get_country_bounds_empty(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = []
        mock_get.return_value = mock_resp
        self.assertIsNone(self.adapter.get_country_bounds("Nowhere"))

    @patch("requests.get")
    def test_get_aircraft_filters_by_country(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"states": [
            ["id1", "CS1", "Germany", 0, 0],
            ["id2", "CS2", "France", 0, 0],
            ["id3", "CS3", "  germany ", 0, 0],
        ]}
        mock_get.return_value = mock_resp

        result = self.adapter.get_aircraft("Germany")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][2], "Germany")
        self.assertEqual(result[1][2], "  germany ")

    @patch("requests.get")
    def test_get_aircraft_empty_states(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"states": []}
        mock_get.return_value = mock_resp
        self.assertEqual(self.adapter.get_aircraft("Germany"), [])

    @patch("requests.get")
    def test_get_aircraft_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("network fail")
        self.assertEqual(self.adapter.get_aircraft("Germany"), [])


if __name__ == "__main__":
    unittest.main()
