# Nim

### Description
An AI that teaches itself to play Nim through reinforcement learning.

In the game Nim, we begin with some number of piles, each with some number of objects. Players take turns: on a player’s turn, the player removes any non-negative number of objects from any one non-empty pile. Whoever removes the last object loses.

<p align="center">
  <img width="400" src="https://user-images.githubusercontent.com/74436899/139157409-dd4471e3-2eaf-4f4e-83e6-e23b6bf05d1e.jpg">
</p>

### Getting Started
1. Visit a demo [here](https://replit.com/@DanielTsiang/nim).
2. Click the green button to run the demo code. Or run ```python play.py```.
3. Wait for AI to finish training itself. The number of games the AI trains on can be modified in ```play.py```.
4. Follow the on-screen instructions!

### Example
```
$ python play.py
Playing training game 1
Playing training game 2
Playing training game 3
...
Playing training game 9999
Playing training game 10000
Done training

Piles:
Pile 0: 1
Pile 1: 3
Pile 2: 5
Pile 3: 7

AI's Turn
AI chose to take 1 from pile 2.
```

### Background
The AI learns the strategy for this game through reinforcement learning. By playing against itself repeatedly and learning from experience, eventually the AI will learn which actions to take and which actions to avoid.

In particular, Q-learning will be used for this project. In Q-learning, we try to learn a reward value (a number) for every ```(state, action)``` pair. An action that loses the game will have a reward of -1, an action that results in the other player losing the game will have a reward of 1, and an action that results in the game continuing has an immediate reward of 0, but will also have some future reward.

A “state” of the Nim game is just the current size of all of the piles. A state, for example, might be ```[1, 1, 3, 5]```, representing the state with 1 object in pile 0, 1 object in pile 1, 3 objects in pile 2, and 5 objects in pile 3.

An “action” in the Nim game will be a pair of integers ```(i, j)```, representing the action of taking ```j``` objects from pile ```i```. So the action ```(3, 5)``` represents the action “from pile 3, take away 5 objects.” Applying that action to the state ```[1, 1, 3, 5]``` would result in the new state ```[1, 1, 3, 0]``` (the same state, but with pile 3 now empty).

The key formula for Q-learning is below. Every time we are in a state ```s``` and take an action ```a```, we can update the Q-value ```Q(s, a)``` according to:

```Q(s, a) <- Q(s, a) + alpha * (new value estimate - old value estimate)```

In the above formula, ```alpha``` is the learning rate (how much we value new information compared to information we already have). The ```new value estimate``` represents the sum of the reward received for the current action and the estimate of all the future rewards that the player will receive. The ```old value estimate``` is just the existing value for ```Q(s, a)```. By applying this formula every time our AI takes a new action, over time the AI will start to learn which actions are better in any state.

### Technologies Used
* Python