import unittest
from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
sentence0 = And(AKnight, AKnave)
knowledge0 = And(
    # each person is either a knight or a knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    # each person cannot be both
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),
    # if person is a knight, then sentence is true, else it is false
    Biconditional(AKnight, sentence0)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
sentence1 = And(AKnave, BKnave)
knowledge1 = And(
    # each person is either a knight or a knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    # each person cannot be both
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),
    # if person is a knight, then sentence is true, else it is false
    Biconditional(AKnight, sentence1)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
sentence2A = Or(And(AKnight, BKnight), And(AKnave, BKnave))
sentence2B = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    # each person is either a knight or a knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    # each person cannot be both
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),
    # if person is a knight, then sentence is true, else it is false
    Biconditional(AKnight, sentence2A),
    Biconditional(BKnight, sentence2B)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
sentence3A = Biconditional(AKnight, Not(AKnave))
sentence3B = And(
    Biconditional(BKnight, AKnave),
    CKnave
)
sentence3C = AKnight
knowledge3 = And(
    # each person is either a knight or a knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    # each person cannot be both
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),
    # if person is a knight, then sentence is true, else it is false
    Biconditional(AKnight, sentence3A),
    Biconditional(BKnight, sentence3B),
    Biconditional(CKnight, sentence3C)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


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
            counter = 0
            for symbol in self.symbols:
                if model_check(knowledge, symbol):
                    message = f"failed for {puzzle}"
                    self.assertEqual(symbol, expected[counter], message)
                    counter += 1


if __name__ == "__main__":
    main()
    unittest.main()
