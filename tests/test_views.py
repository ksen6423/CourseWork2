import unittest
import os
import json
import tempfile
from unittest.mock import patch, MagicMock

from src.views import JSONStorage


class TestJSONStorage(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp.close()
        os.remove(self.tmp.name)
        self.storage = JSONStorage(self.tmp.name)

    def tearDown(self):
        if os.path.exists(self.tmp.name):
            os.remove(self.tmp.name)

    def test_init_creates_file(self):
        self.assertTrue(os.path.exists(self.tmp.name))
        with open(self.tmp.name, encoding="utf-8") as f:
            self.assertEqual(json.load(f), [])

    def test_read_corrupted(self):
        with open(self.tmp.name, "w", encoding="utf-8") as f:
            f.write("not json")
        self.assertEqual(self.storage._read_file(), [])

    def test_add_aircraft(self):
        plane = MagicMock()
        plane.callsign, plane.country = "CS1", "France"
        plane.velocity, plane.altitude = 200.0, 10000.0
        plane.to_dict.return_value = {"callsign": "CS1", "country": "France",
                                      "velocity": 200.0, "altitude": 10000.0}
        self.storage.add_aircraft(plane)
        with open(self.tmp.name, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["callsign"], "CS1")

    def test_delete_by_callsign(self):
        with open(self.tmp.name, "w", encoding="utf-8") as f:
            json.dump([{"callsign": "A"}, {"callsign": "B"}], f)
        self.storage.delete_aeroplane("A")
        with open(self.tmp.name, encoding="utf-8") as f:
            self.assertEqual(json.load(f), [{"callsign": "B"}])

    def test_get_by_country(self):
        with open(self.tmp.name, "w", encoding="utf-8") as f:
            json.dump([{"callsign": "A", "origin_country": "France",
                        "velocity": 100.0, "geo_altitude": 5000.0}], f)
        result = self.storage.get_by_country("France")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].callsign, "A")

    @patch("src.aeroplane.Aeroplane")
    def test_get_aeroplanes_criteria(self, mock_plane):
        with open(self.tmp.name, "w", encoding="utf-8") as f:
            json.dump([{"callsign": "A", "origin_country": "France",
                        "velocity": 1.0, "geo_altitude": 2.0}], f)
        mock_plane.return_value.origin_country = "France"
        result = self.storage.get_aeroplanes(criteria={"origin_country": "France"})
        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
