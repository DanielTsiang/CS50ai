import sys
import unittest
from unittest.mock import patch
from pathlib import Path
import numpy as np

from shopping import find_predictions


class Test(unittest.TestCase):
    """
    Unit test for shopping.csv data.
    Usage: python test_shopping.py
    """

    @classmethod
    def setUpClass(cls):
        cls.expected_correct = 4082
        cls.expected_incorrect = 850
        cls.expected_true_positive_rate = 41.0
        cls.expected_true_negative_rate = 90.0

        # Mock `sys.argv` using `patch.object()`
        with patch.object(sys, "argv", [Path(__file__).name, "shopping.csv"]):
            y_test, predictions, sensitivity, specificity = find_predictions()

            cls.actual_correct = sum(i == j for i, j in zip(y_test, predictions))
            cls.actual_incorrect = sum(i != j for i, j in zip(y_test, predictions))
            cls.actual_true_positive_rate = 100 * sensitivity
            cls.actual_true_negative_rate = 100 * specificity

    def test_correct(self):
        np.testing.assert_allclose(self.actual_correct, self.expected_correct, rtol=0.02)

    def test_incorrect(self):
        np.testing.assert_allclose(self.actual_incorrect, self.expected_incorrect, rtol=0.05)

    def test_true_positive_rate(self):
        np.testing.assert_allclose(self.actual_true_positive_rate, self.expected_true_positive_rate, atol=6)

    def test_true_negative_rate(self):
        np.testing.assert_allclose(self.actual_true_negative_rate, self.expected_true_negative_rate, atol=2)


if __name__ == "__main__":
    unittest.main()
