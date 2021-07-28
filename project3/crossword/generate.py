import sys
from collections import deque

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def string(self, assignment):
        letters = self.letter_grid(assignment)
        string = "\n"
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                string += letters[i][j] if self.crossword.structure[i][j] else "█"
            string += "\n"
        return string
    
    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable, words in self.domains.items():
            words_to_remove = set()
            for word in words:
                # Ensure every value in a variable’s domain has the same
                # number of letters as the variable’s length.
                if len(word) != variable.length:
                    words_to_remove.add(word)
                # Subtract unsuitable words from variable's domain
                self.domains[variable] = words.difference(words_to_remove)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        A conflict in the context of the crossword puzzle is a square for which
        two variables disagree on what character value it should take on.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]

        if overlap:
            i, j = overlap
            #  Remove any value from the domain of x that disagrees with y
            x_words_to_remove = set()
            for x_word in self.domains[x]:
                # check if there is any value in x variable that overlaps with value in y variable
                overlap_possible = any(
                    x_word != y_word and x_word[i] == y_word[j]
                    for y_word in self.domains[y]
                )

                # no overlap possible, so remove value from x variable
                if not overlap_possible:
                    x_words_to_remove.add(x_word)

            if x_words_to_remove:
                self.domains[x] = self.domains[x].difference(x_words_to_remove)
                revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            # Initial deque (Doubly Ended Queue) of all of the arcs
            arcs = deque()
            for variable1 in self.crossword.variables:
                for variable2 in self.crossword.neighbors(variable1):
                    arcs.append((variable1, variable2))
        else:
            arcs = deque(arcs)

        while arcs:
            x, y = arcs.popleft()
            if self.revise(x, y):
                # Problem is unsolvable,
                # as no more possible values for variable x.
                if len(self.domains[x]) == 0:
                    return False
                # Add additional arcs to queue,
                # to ensure that other arcs stay consistent.
                for neighbor in self.crossword.neighbors(x) - {y}:
                    arcs.append((neighbor, x))

        # Arc consistency is enforced
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return not any(
            variable not in assignment
            or assignment[variable] not in self.crossword.words
            for variable in self.crossword.variables
        )

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for variable1, word1 in assignment.items():
            # Ensure every value is the correct length
            if len(word1) != variable1.length:
                return False

            # Ensure all values are distinct
            for variable2, word2 in assignment.items():
                if variable1 != variable2:
                    if word1 == word2:
                        return False

                    # Ensure there are no conflict between variables
                    overlap = self.crossword.overlaps[variable1, variable2]
                    if overlap:
                        i, j = overlap
                        # Check for conflicting characters
                        if word1[i] != word2[j]:
                            return False

        # Assignment is consistent
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Find all the neighbors of the given variable
        neighbors = self.crossword.neighbors(var)

        # Traverse over the assignment and see if some neighboring variables are already assigned a word
        for variable in assignment:
            # If variable is in neighbors and in assignment,
            # it already has a value and is not considered a neighbor
            if variable in neighbors:
                neighbors.remove(variable)

        # Initialise a result list that will be sorted according to a heuristic (least-constraining values)
        result = []
        for word1 in self.domains[var]:
            # Keep count of how many domain options will be ruled out from neighboring variables
            ruled_out = 0
            for neighbor in neighbors:
                for word2 in self.domains[neighbor]:
                    overlap = self.crossword.overlaps[var, neighbor]

                    # If inconsistency in overlap, then need to remove word from one of the variable's domain
                    if overlap:
                        i, j = overlap
                        if word1[i] != word2[j]:
                            ruled_out += 1

            # Store the variable with the number of options it will rule out from its neighbors
            result.append([word1, ruled_out])

        # Sort variables by the number of ruled out domain options
        result.sort(key=lambda x: x[1])

        # Return only the list of variables, without the ruled_out parameter
        return [i[0] for i in result]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Initialise a list of potential variables to consider with heuristics (minimum remaining value and degrees)
        potential_variables = [
            [
                variable,
                len(self.domains[variable]),
                len(self.crossword.neighbors(variable)),
            ]
            for variable in self.crossword.variables
            if variable not in assignment
        ]

        # Sort potential variables by the number of domain options (ascending) and number of neighbors (descending)
        if potential_variables:
            potential_variables.sort(key=lambda x: (x[1], -x[2]))
            return potential_variables[0][0]

        # If there are no potential variables, simply return None
        return None

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if assignment is complete
        if self.assignment_complete(assignment):
            return assignment

        # Select an unassigned variable to choose a word from its domain
        variable = self.select_unassigned_variable(assignment)

        # Traverse over all the values in the domain that is sorted with a heuristic (least constraining values)
        for value in self.order_domain_values(variable, assignment):
            new_assignment = assignment.copy()
            new_assignment[variable] = value

            # Queue of all arcs (Y, X) where Y is a neighbor of X
            neighbors = self.crossword.neighbors(variable)
            arcs = [(neighbor, variable) for neighbor in neighbors]
            # Interleave backtracking search with inference
            # i.e. reinforce arc-consistency (Maintaining Arc-Consistency algorithm)
            self.ac3(arcs)

            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result

        # No satisfying assignment is possible
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)
        return creator.string(assignment)

if __name__ == "__main__":
    main()
