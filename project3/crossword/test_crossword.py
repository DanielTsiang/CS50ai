import unittest
import sys
from unittest.mock import patch
from pathlib import Path

from generate import generate_crossword
from test_resources.expected_results import data0, data1


class Test(unittest.TestCase):
    """
    Unit test for generating crosswords.
    Usage: python test_crossword.py
    """

    def setUp(self):
        self.data_set = {
            "data0": [31, data0],
            "data1": [136, data1],
            "data2": 49
        }

    def test_generate(self):
        for i, data in enumerate(self.data_set):
            # Mock `sys.argv` using `patch.object()`
            with patch.object(sys, "argv", [Path(__file__).name, f"data/structure{i}.txt", f"data/words{i}.txt"]):
                with self.subTest(data=data):
                    creator, assignment, _ = generate_crossword()
                    result = creator.string(assignment)

                    error_message = f"\nFailed for structure 'data/structure{i}.txt' and words 'data/words{i}.txt'."
                    if isinstance(self.data_set[data], list):
                        expected_length = self.data_set[data][0]
                        expected_crossword = self.data_set[data][1]

                        error_message0 = error_message + f"\nExpected {expected_length} but calculated {len(result)}."
                        self.assertEqual(expected_length, len(result), error_message0)

                        error_message1 = error_message + f"\nExpected {expected_crossword} but calculated {result}."
                        self.assertIn(result, expected_crossword, error_message1)

                    else:
                        expected_length = self.data_set[data]
                        error_message0 = error_message + f"\nExpected {expected_length} but calculated {len(result)}."
                        self.assertEqual(expected_length, len(result), error_message0)


if __name__ == "__main__":
    # run unit test
    unittest.main()
