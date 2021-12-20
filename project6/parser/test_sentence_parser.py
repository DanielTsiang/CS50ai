import os
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

from nltk.tree import Tree
from sentence_parser import parser, preprocess, get_noun_phrase_chunks


class Test(unittest.TestCase):
    """
    Unit test for sentence_parser.py.
    Usage: python test_sentence_parser.py
    """

    def setUp(self) -> None:
        self.expected_noun_phrase_chunks = {
            1: [Tree('NP', [Tree('N', ['holmes'])])],
            2: [Tree('NP', [Tree('N', ['holmes'])]), Tree('NP', [Tree('Det', ['a']), Tree('N', ['pipe'])])],
            3: [Tree('NP', [Tree('N', ['we'])]), Tree('NP', [Tree('Det', ['the']), Tree('N', ['day'])]), Tree('NP', [Tree('N', ['thursday'])])],
            4: [Tree('NP', [Tree('N', ['holmes'])]), Tree('NP', [Tree('Det', ['the']), Tree('AP', [Tree('Adj', ['red']), Tree('N', ['armchair'])])]), Tree('NP', [Tree('N', ['he'])])],
            5: [Tree('NP', [Tree('Det', ['my']), Tree('N', ['companion'])]), Tree('NP', [Tree('Det', ['an']), Tree('AP', [Tree('Adj', ['enigmatical']), Tree('N', ['smile'])])])],
            6: [Tree('NP', [Tree('N', ['holmes'])]), Tree('NP', [Tree('N', ['himself'])])],
            7: [Tree('NP', [Tree('N', ['she'])]), Tree('NP', [Tree('Det', ['a']), Tree('N', ['word'])]), Tree('NP', [Tree('N', ['we'])]), Tree('NP', [Tree('Det', ['the']), Tree('N', ['door'])])],
            8: [Tree('NP', [Tree('N', ['holmes'])]), Tree('NP', [Tree('Det', ['his']), Tree('N', ['pipe'])])],
            9: [Tree('NP', [Tree('N', ['i'])]), Tree('NP', [Tree('Det', ['a']), Tree('AP', [Tree('Adj', ['country']), Tree('N', ['walk'])])]), Tree('NP', [Tree('N', ['thursday'])]), Tree('NP', [Tree('N', ['home'])]), Tree('NP', [Tree('Det', ['a']), Tree('AP', [Tree('Adj', ['dreadful']), Tree('N', ['mess'])])])],
            10: [Tree('NP', [Tree('N', ['i'])]), Tree('NP', [Tree('Det', ['a']), Tree('AP', [Tree('Adj', ['little']), Tree('AP', [Tree('Adj', ['moist']), Tree('AP', [Tree('Adj', ['red']), Tree('N', ['paint'])])])])]), Tree('NP', [Tree('Det', ['the']), Tree('N', ['palm'])]), Tree('NP', [Tree('Det', ['my']), Tree('N', ['hand'])])],
        }
        self.max_sentences = 10
        self.sentences_directory = "sentences"

    def test_sentence_parser(self):
        # Mock `sys.argv` using `patch.object()`
        with patch.object(sys, "argv", [Path(__file__).name, self.sentences_directory]):
            for i in range(1, self.max_sentences + 1):
                with self.subTest(sentence=f"{i}.txt"):
                    with open(os.path.join(self.sentences_directory, f"{i}.txt")) as file:
                        sentence = file.read()

                    # Convert input into list of words
                    sentence = preprocess(sentence)

                    # Attempt to parse sentence
                    trees = list(parser.parse(sentence))

                    actual_noun_phrase_chunks = get_noun_phrase_chunks(trees[0])
                    message = f"\nExpected noun phrase chunks: {self.expected_noun_phrase_chunks[i]}" \
                              f"\nActual noun phrase chunks: {actual_noun_phrase_chunks}."
                    self.assertEqual(self.expected_noun_phrase_chunks[i], actual_noun_phrase_chunks, msg=message)


if __name__ == "__main__":
    unittest.main()
