import unittest
from unittest.mock import patch
import sys

from heredity import find_probabilities
from test_resources.expected_results import family0, family1, family2


class Test(unittest.TestCase):
    """
    Unit test for 3 sets of family data.
    Usage: python test_heredity.py
    """

    def setUp(self):
        self.families = {
            "data/family0.csv": family0,
            "data/family1.csv": family1,
            "data/family2.csv": family2,
        }

    def test_heredity(self):
        for family in self.families:
            # Substitute `sys.argv` using `patch.object()`
            with patch.object(sys, "argv", [__name__, family]):
                probabilities = find_probabilities()[0]
                for person in probabilities:
                    for field in probabilities[person]:
                        for value in probabilities[person][field]:
                            with self.subTest(family=family[5:12], person=person, field=field, value=value):
                                result = round(probabilities[person][field][value], 4)
                                expected = self.families[family][person][field][value]
                                message = f"\nFailed for {family[5:12]}, {person}, " \
                                          f"{field.capitalize()}: {value}" \
                                          f"\nExpected {expected} but calculated {result}"
                                self.assertEqual(result, expected, message)


if __name__ == "__main__":
    unittest.main()
