import unittest
import sys
from heredity import main


class Test(unittest.TestCase):
    """
    Unit test for family0 data.
    Usage: python test0.py data/family0.csv
    """
    family0 = {

        "Harry": {

            "gene": {
                2: 0.0092,
                1: 0.4557,
                0: 0.5351
            },

            "trait": {
                True: 0.2665,
                False: 0.7335
            }
        },

        "James": {

            "gene": {
                2: 0.1976,
                1: 0.5106,
                0: 0.2918
            },

            "trait": {
                True: 1.0,
                False: 0.0
            }
        },

        "Lily": {

            "gene": {
                2: 0.0036,
                1: 0.0136,
                0: 0.9827
            },

            'trait': {
                True: 0.0,
                False: 1.0
            }
        }
    }

    def test_heredity(self):
        probabilities = main()
        for person in probabilities:
            for field in probabilities[person]:
                for value in probabilities[person][field]:
                    result = round(probabilities[person][field][value], 4)
                    expected = self.family0[person][field][value]
                    message = f"\nFailed for {person}, {field.capitalize()}: {value} \nExpected {expected} but calculated {result}"
                    self.assertEqual(result, expected, message)


if __name__ == "__main__":
    # Check for proper usage
    if len(sys.argv) != 2 or sys.argv[1] != "data/family0.csv":
        sys.exit("Usage: python test0.py data/family0.csv")

    # run unit test
    unittest.main(argv=[sys.argv[0]])