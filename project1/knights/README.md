# "Knights and Knaves" Logic Puzzles

### Description
A program that solves logic puzzles. The puzzles are represented using propositional logic, enabling the AI to solve them using a model-checking algorithm.

### Background
In a Knights and Knaves puzzle, the following information is given: Each character is either a knight or a knave. A knight will always tell the truth: if knight states a sentence, then that sentence is true.
Conversely, a knave will always lie: if a knave states a sentence, then that sentence is false.

The objective of the puzzle is, given a set of sentences spoken by each of the characters, determine, for each character, whether that character is a knight or a knave.

<p align="center">
  <img width="318" src="https://user-images.githubusercontent.com/74436899/124282635-f46c6100-db42-11eb-905f-eaf3eba882b1.png">
</p>

### Getting Started
1. Visit a demo [here](https://replit.com/@DanielTsiang/logic-puzzles).
2. Click the green button to run the demo code. Or run ```python puzzle.py```.
3. View the answers in the terminal.
4. A unit test can be run via ```python test_puzzle.py```.

### Puzzles
* Puzzle 0 contains a single character, A.
    * A says “I am both a knight and a knave.”
* Puzzle 1 has two characters: A and B.
    * A says “We are both knaves.”
    * B says nothing.
* Puzzle 2 has two characters: A and B.
    * A says “We are the same kind.”
    * B says “We are of different kinds.”
* Puzzle 3 has three characters: A, B, and C.
    * A says either “I am a knight.” or “I am a knave.”, but you don’t know which.
    * B says “A said ‘I am a knave.’”
    * B then says “C is a knave.”
    * C says “A is a knight.”

### Technologies Used
* Python
