import unittest

from src.aeroplane import Aeroplane


class TestAeroplane(unittest.TestCase):

    def test_init_and_validation(self):
        # Проверка корректного создания объекта
        plane = Aeroplane("UAL123", "USA", 250.5, 10000)
        self.assertEqual(plane.callsign, "UAL123")
        self.assertEqual(plane.country, "USA")
        self.assertEqual(plane.velocity, 250.5)
        self.assertEqual(plane.geo_altitude, 10000)

        # Проверка на ValueError при отрицательных значениях
        with self.assertRaises(ValueError):
            Aeroplane("TEST", "UK", -100, 5000)
        with self.assertRaises(ValueError):
            Aeroplane("TEST", "UK", 100, -5000)

    def test_comparison_methods(self):
        plane1 = Aeroplane("A1", "CountryA", 200, 8000)
        plane2 = Aeroplane("A2", "CountryB", 220, 9000)
        plane3 = Aeroplane("A3", "CountryC", 200, 8000)

        # Проверка __lt__ (меньше)
        self.assertTrue(plane1 < plane2)
        self.assertFalse(plane2 < plane1)

        self.assertTrue(plane2 > plane1)
        self.assertFalse(plane1 > plane2)

        self.assertTrue(plane1 == plane3)
        self.assertFalse(plane1 == plane2)

    def test_str_method(self):
        plane = Aeroplane("B737", "Germany", 230, 9500)
        self.assertEqual(str(plane), "Самолет: B737")

    def test_to_dict_method(self):
        plane = Aeroplane("AFR567", "France", 260, 11000)
        expected_dict = {"callsign": "AFR567", "country": "France", "velocity": 260.0, "geo_altitude": 11000.0}
        self.assertEqual(plane.to_dict(), expected_dict)


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
