from nim import train, play

# The train function trains an AI by running n simulated games against itself, returning the fully trained AI.
ai = train(10000)

while True:
    # The play function accepts a trained AI as input, and lets a human player play a game of Nim against the AI.
    ai = play(ai)

    i = input("Play another game? [Y/n]: ")
    if i.lower() in ["n", "no"]:
        break
    print("New game started:")

print("Game exited. Thanks for playing!")
