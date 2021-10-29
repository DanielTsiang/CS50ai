import unittest
from puzzle import *


class Test(unittest.TestCase):
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0, [AKnave]),
        ("Puzzle 1", knowledge1, [AKnave, BKnight]),
        ("Puzzle 2", knowledge2, [AKnave, BKnight]),
        ("Puzzle 3", knowledge3, [AKnight, BKnave, CKnight])
    ]

    def test_puzzles(self):
        for puzzle, knowledge, expected in self.puzzles:
            with self.subTest(puzzle=puzzle):
                counter = 0
                for symbol in self.symbols:
                    if model_check(knowledge, symbol):
                        message = f"failed for {puzzle}"
                        self.assertEqual(symbol, expected[counter], message)
                        counter += 1


if __name__ == "__main__":
    unittest.main()