import sys
import unittest
from unittest.mock import patch
from pathlib import Path
import numpy as np
from sklearn.metrics import classification_report

from shopping import predict_labels


class Test(unittest.TestCase):
    """
    Unit test for shopping.csv data.
    Usage: python test_shopping.py
    """

    @classmethod
    def setUpClass(cls):
        cls.expected_accuracy = 0.889
        cls.expected_true_positive_rate = 0.561
        cls.expected_true_negative_rate = 0.949

        # Mock `sys.argv` using `patch.object()`
        with patch.object(sys, "argv", [Path(__file__).name, "shopping.csv"]):
            y_test, y_pred = predict_labels()

            # Evaluate model performance
            report = classification_report(y_test, y_pred, output_dict=True)

            cls.actual_accuracy = report['accuracy']
            cls.actual_true_positive_rate = report['1']['recall']
            cls.actual_true_negative_rate = report['0']['recall']

    def test_accuracy(self):
        np.testing.assert_approx_equal(self.actual_accuracy, self.expected_accuracy, significant=3)

    def test_true_positive_rate(self):
        np.testing.assert_approx_equal(self.actual_true_positive_rate, self.expected_true_positive_rate, significant=3)

    def test_true_negative_rate(self):
        np.testing.assert_approx_equal(self.actual_true_negative_rate, self.expected_true_negative_rate, significant=3)


if __name__ == "__main__":
    unittest.main()
