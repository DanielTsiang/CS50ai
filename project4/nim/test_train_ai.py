import unittest
from contextlib import redirect_stdout
from io import StringIO

from nim import train


class Test(unittest.TestCase):
    """
    Unit test for training Nim AI.
    """
    def setUp(self):
        self.games_trained = 1000

    def test_train(self):
        # Suppress print statements to stdout
        with redirect_stdout(StringIO()):
            ai = train(self.games_trained)

        # Assert that the Q-learning dictionary for the Nim AI is not empty
        error_message = "Q-learning dictionary is empty"
        self.assertTrue(ai.q, error_message)


if __name__ == "__main__":
    unittest.main()
