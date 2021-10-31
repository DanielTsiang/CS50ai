import unittest

from degrees import shortest_path, load_data, person_id_for_name


class Test(unittest.TestCase):

    def setUp(self):
        self.test_cases = [
            ("Kevin Bacon", "Tom Cruise", 1, [("104257", "129")]),
            ("Tom Cruise", "Tom Hanks", 2, [("104257", "102"), ("112384", "158")]),
            ("Kevin Bacon", "Emma Watson", 0, None),
        ]

        self.directory = "small"

    def test_degrees(self):
        for source, target, expected_degrees, expected_path in self.test_cases:
            with self.subTest(source=source, target=target):
                load_data(self.directory)
                actual_path = shortest_path(person_id_for_name(source), person_id_for_name(target))
                actual_degrees = len(actual_path) if actual_path is not None else 0
                error_message = f"\nFailed for {source} as source, and {target} as target." \
                                f"\nExpected {expected_degrees} degrees of separation but calculated {actual_degrees}."
                self.assertEqual(expected_degrees, actual_degrees, msg=error_message)
                self.assertEqual(expected_path, actual_path, msg=error_message.split(".")[0])


if __name__ == "__main__":
    unittest.main()
