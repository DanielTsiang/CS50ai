import sys
import unittest
from unittest.mock import patch
from pathlib import Path

from answerbot import get_file_idfs, get_top_sentence_matches, tokenize


class Test(unittest.TestCase):
    """
    Unit test answerbot.py.
    Usage: python test_answerbot.py
    """

    def setUp(self) -> None:
        self.queries = [
            "What are the types of supervised learning?",
            "When was Python 3.0 released?",
            "How do neurons connect in a neural network?",
        ]
        self.answers = [
            "Types of supervised learning algorithms include Active learning, classification and regression.",
            "Python 3.0 was released on 3 December 2008.",
            "Neurons of one layer connect only to neurons of the immediately preceding and immediately following layers.",
        ]
        self.SENTENCE_MATCHES = 1
        self.corpus_directory = "corpus"

    def test_answerbot(self):
        # Mock `sys.argv` using `patch.object()`
        with patch.object(sys, "argv", [Path(__file__).name, self.corpus_directory]):
            files, file_words, file_idfs = get_file_idfs()
            for i in range(len(self.queries)):
                with self.subTest(query=self.queries[i]):
                    query = set(tokenize(self.queries[i]))
                    matches = get_top_sentence_matches(query, files, file_words, file_idfs)
                    expected = self.answers[i]
                    message = f"\nExpected sentence: {self.answers[i]}" \
                              f"\nActual sentence: {matches[:self.SENTENCE_MATCHES]}."
                    self.assertEqual(expected, matches[:self.SENTENCE_MATCHES][0], msg=message)


if __name__ == "__main__":
    unittest.main()
