import unittest
import sys
from unittest.mock import patch
from pathlib import Path

from generate import generate_crossword
from test_resources.expected_results import data1


class Test(unittest.TestCase):
    """
    Unit test for generating crosswords.
    Usage: python test_crossword.py
    """

    def setUp(self):
        self.data_set = {
            "data1": data1,
        }

    def test_generate(self):
        for i, data in enumerate(self.data_set, 1):
            # Mock `sys.argv` using `patch.object()`
            with patch.object(sys, "argv", [Path(__file__).name, f"data/structure{i}.txt", f"data/words{i}.txt"]):
                with self.subTest(data=data):
                    creator, assignment, _ = generate_crossword()
                    result = creator.string(assignment)
                    expected = self.data_set[data]
                    message = f"\nFailed for structure '{sys.argv[1]}' and words '{sys.argv[2]}'." \
                              f"\nExpected {expected} but calculated {result}."
                    self.assertIn(result, expected, message)


if __name__ == "__main__":
    # run unit test
    unittest.main()
