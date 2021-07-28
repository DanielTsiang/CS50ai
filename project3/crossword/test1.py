import unittest
import sys
from generate import main


class Test(unittest.TestCase):
    """
    Unit test for structure1 and words1 data set.
    Usage: python generate.py data/structure1.txt data/words1.txt [output1.png]
    """
    output1_a = """
██████████████
███████M████R█
█INTELLIGENCE█
█N█████N████S█
█F██LOGIC███O█
█E█████M████L█
█R███SEARCH█V█
███████X████E█
██████████████
"""

    output1_b = """
██████████████
███████M████R█
█INTELLIGENCE█
█N█████N████S█
█F██LOGIC███O█
█E█████M████L█
█R███REASON█V█
███████X████E█
██████████████
"""

    output1_c = """
██████████████
███████M████N█
█INTELLIGENCE█
█N█████N████T█
█F██LOGIC███W█
█E█████M████O█
█R███SEARCH█R█
███████X████K█
██████████████
"""

    output1_d = """
██████████████
███████M████N█
█INTELLIGENCE█
█N█████N████T█
█F██LOGIC███W█
█E█████M████O█
█R███REASON█R█
███████X████K█
██████████████
"""

    def test_generate(self):
        result = main()
        expected = [self.output1_a, self.output1_b, self.output1_c, self.output1_d]
        message = f"\nFailed for structure '{sys.argv[1]}' and words '{sys.argv[2]}'.\nExpected {expected} but calculated {result}."
        self.assertIn(result, expected, message)


if __name__ == "__main__":
    # Check for proper usage
    if len(sys.argv) not in [3, 4] or sys.argv[1] != "data/structure1.txt" or sys.argv[2] != "data/words1.txt":
        sys.exit("Usage: python test1.py data/structure1.txt data/words1.txt [output1.png]")

    # run unit test
    unittest.main(argv=[sys.argv[0]])