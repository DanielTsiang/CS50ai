# Minesweeper AI

### Description
An AI that plays Minesweeper.

Knowledge is represented as a logical sentence with two parts: a set of cells on the board that are involved in the sentence, and a number count, representing the count of how many of those cells are mines. Subtraction of sets allows knowledge to be inferred and new conclusions to be drawn.

### Getting Started
1. Visit a demo [here](https://replit.com/@DanielTsiang/minesweeper).
2. Click the green button to run the demo code. Or run ```python runner.py```.
3. Click once, or hold down the click button, on the "AI Move" button for the AI to make one or multiple moves respectively.
4. As the game progresses, information such as detected mines is displayed in the terminal. The player can intervene manually, e.g. right-click onto the cell to display the flag icon but this is optional.
5. If the game is won, all of the flag icons will automatically be displayed.
6. If the game is lost, i.e. because a bomb was clicked on, all of the bomb icons will automatically be displayed.
7. Click the reset button to reset the board and play another game.

### Example
<p align="center">
  <img width="712" src="https://user-images.githubusercontent.com/74436899/124366273-6e394300-dc46-11eb-9b61-e256c8f964e4.png">
</p>

### Background
Minesweeper is a puzzle game that consists of a grid of cells, where some of the cells contain hidden “mines.” Clicking on a cell that contains a mine detonates the mine, and causes the user to lose the game. Clicking on a “safe” cell (i.e., a cell that does not contain a mine) reveals a number that indicates how many neighbouring cells – where a neighbour is a cell that is one square to the left, right, up, down, or diagonal from the given cell – contain a mine.

The goal of the game is to flag (i.e., identify) each of the mines. In many implementations of the game, including the one in this project, the player can flag a mine by right-clicking on a cell (or two-finger clicking, depending on the computer).

### Technologies Used
* Python with Pygame
