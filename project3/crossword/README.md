# Crossword

### Description
An AI that generates crossword puzzles.

Given the structure of a crossword puzzle and a list of words to use, the AI chooses which words should go in each vertical or horizontal sequence of squares. This problem is modelled as a constraint satisfaction problem.

<p align="center">
  <img width="500" src="https://user-images.githubusercontent.com/74436899/126911331-167fe531-5897-414d-ad91-b0180219f9ec.png">
</p>

### Getting Started
1. Visit a demo [here](https://replit.com/@DanielTsiang/crossword#README.md).
2. Click the green button to run the demo code for the ```structure1``` structure and ```words1``` data set.
3. The generated crossword puzzle can be viewed in the picture named ```output1.png```.
4. Alternatively run ```python generate.py data/structure0.txt data/words0.txt output0.png``` or ```python generate.py data/structure2.txt data/words2.txt output2.png``` or any other combination, to generate crossword puzzles for other structures and data sets.
5. Unit tests for all 3 data sets can be run via ```python test_crossword.py ```.

### Example
Example with the ```structure1``` structure and ```words1``` data set:
```
$ python generate.py data/structure1.txt data/words1.txt output.png
██████████████
███████M████R█
█INTELLIGENCE█
█N█████N████S█
█F██LOGIC███O█
█E█████M████L█
█R███SEARCH█V█
███████X████E█
██████████████
```

### Background
How might you go about generating a crossword puzzle? Given the structure of a crossword puzzle (i.e., which squares of the grid are meant to be filled in with a letter), and a list of words to use, the problem becomes one of choosing which words should go in each vertical or horizontal sequence of squares. We can model this sort of problem as a constraint satisfaction problem. Each sequence of squares is one variable, for which we need to decide on its value (which word in the domain of possible words will fill in that sequence). Consider the following crossword puzzle structure.

<p align="left">
  <img width="300" src="https://user-images.githubusercontent.com/74436899/126911566-6388c84b-ef67-43bf-8560-28c577f8da2d.png">
</p>

In this structure, we have four variables, representing the four words we need to fill into this crossword puzzle (each indicated by a number in the above image). Each variable is defined by four values: the row it begins on (its ```i``` value), the column it begins on (its ```j``` value), the direction of the word (either down or across), and the length of the word. Variable 1, for example, would be a variable represented by a row of ```1``` (assuming ```0``` indexed counting from the top), a column of ```1``` (also assuming ```0``` indexed counting from the left), a direction of ```across```, and a length of ```4```.

As with many constraint satisfaction problems, these variables have both unary and binary constraints. The unary constraint on a variable is given by its length. For Variable 1, for instance, the value ```BYTE``` would satisfy the unary constraint, but the value ```BIT``` would not (it has the wrong number of letters). Any values that don’t satisfy a variable’s unary constraints can therefore be removed from the variable’s domain immediately.

The binary constraints on a variable are given by its overlap with neighboring variables. Variable 1 has a single neighbor: Variable 2. Variable 2 has two neighbors: Variable 1 and Variable 3. For each pair of neighboring variables, those variables share an overlap: a single square that is common to them both. We can represent that overlap as the character index in each variable’s word that must be the same character. For example, the overlap between Variable 1 and Variable 2 might be represented as the pair ```(1, 0)```, meaning that Variable 1’s character at index 1 necessarily must be the same as Variable 2’s character at index 0 (assuming 0-indexing, again). The overlap between Variable 2 and Variable 3 would therefore be represented as the pair ```(3, 1)```: character 3 of Variable 2’s value must be the same as character 1 of Variable 3’s value.

For this problem, we’ll add the additional constraint that all words must be different: the same word should not be repeated multiple times in the puzzle.

The challenge ahead, then, is to write a program to find a satisfying assignment: a different word (from a given vocabulary list) for each variable such that all the unary and binary constraints are met.

### Technologies Used
* Python