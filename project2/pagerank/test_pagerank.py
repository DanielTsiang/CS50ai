import sys
import unittest
from unittest.mock import patch
from pathlib import Path

from pagerank import crawl, sample_pagerank, iterate_pagerank, DAMPING, SAMPLES
from test_resources.expected_results import corpus0, corpus1, corpus2


class Test(unittest.TestCase):
    """
    Unit test for 3 sets of family data.
    Usage: python test_heredity.py
    """

    @classmethod
    def setUpClass(cls):
        cls.corpuses = {
            "corpus0": corpus0,
            "corpus1": corpus1,
            "corpus2": corpus2
        }

    def test_sample(self):
        for corpus in self.corpuses:
            # Mock `sys.argv` using `patch.object()`
            with patch.object(sys, "argv", [Path(__file__).name, corpus]):
                crawled_corpus = crawl(corpus)
                ranks = sample_pagerank(crawled_corpus, DAMPING, SAMPLES)
                for page in sorted(ranks):
                    with self.subTest(corpus=corpus, page=page):
                        expected = self.corpuses[corpus][page]
                        message = f"\nSample method failed for {corpus}, {page}" \
                                  f"\nExpected around {expected} but calculated {ranks[page]}."
                        self.assertAlmostEqual(ranks[page], expected, places=1, msg=message)

    def test_iterate(self):
        for corpus in self.corpuses:
            # Mock `sys.argv` using `patch.object()`
            with patch.object(sys, "argv", [Path(__file__).name, corpus]):
                crawled_corpus = crawl(corpus)
                ranks = iterate_pagerank(crawled_corpus, DAMPING)[0]
                for page in sorted(ranks):
                    with self.subTest(corpus=corpus, page=page):
                        expected = self.corpuses[corpus][page]
                        message = f"\nIterate method failed for {corpus}, {page}" \
                                  f"\nExpected {expected} but calculated {ranks[page]}."
                        self.assertAlmostEqual(ranks[page], expected, places=4, msg=message)


if __name__ == "__main__":
    unittest.main()
