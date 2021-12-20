import nltk
import os
from pathlib import Path
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> S Conj S | S Conj VP | NP VP
AP -> Adj N | Adj AP
NP -> N | AP | Det AP | Det N 
PP -> P NP | PP PP
VP -> V | V NP | V PP | V NP PP | Adv VP | VP Adv
"""

nltk.data.path.append(os.path.join(Path(__file__).resolve().parent, "nltk_data"))
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)
sentence_path = os.path.join(Path(__file__).resolve().parent, "sentences")


def main(select_premade_sentence: bool = False):

    # If filename specified, read sentence from file
    if len(sys.argv) == 2 and not select_premade_sentence:
        with open(sys.argv[1]) as file:
            sentence = file.read()

    # Ask user to input an int to select from pre-made sentences
    elif len(sys.argv) == 2:
        sentence_number = get_valid_int()
        with open(os.path.join(sentence_path, f"{sentence_number}.txt")) as file:
            sentence = file.read()

    # Otherwise, get sentence as input
    else:
        sentence = input("Enter sentence: ")

    # Convert input into list of words
    sentence = preprocess(sentence)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(sentence))
    except ValueError as error:
        print(error)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        print("Tree:")
        tree.pretty_print()

        print("Noun Phrase Chunks:")
        for noun_phrase in get_noun_phrase_chunks(tree):
            print("    " + " ".join(noun_phrase.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase and removing any word that does not contain at least
    one alphabetic character.
    """
    return [
        word.lower()
        for word in nltk.word_tokenize(sentence)
        if any(char.isalpha() for char in word)
    ]


def get_noun_phrase_chunks(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence whose label is "NP" that does not itself contain any
    other noun phrases as subtrees.
    """
    return [
        subtree
        for subtree in tree.subtrees()
        if subtree.label() == "NP"
    ]


def ask_user_if_continue():
    """Ask the user if they would like to parse another sentence."""
    user_input = input("Parse another sentence? [Y/n]: ")
    return user_input.lower() not in ["n", "no"]


def get_valid_int():
    """Check if an `input` is a positive integer and within a specific range."""
    max_value = 10
    while True:
        try:
            user_input = int(input("Enter a number between 1-10 to select a pre-made sentence to parse: "))
        except ValueError:
            print("That is not a valid integer.")
            continue
        else:
            if 1 <= user_input <= max_value:
                return user_input
            print("Number entered is not within the valid range.")
            continue


if __name__ == "__main__":
    # Initialize Boolean flag to True as default
    continue_program = True

    # If user supplied a path to a text file
    if len(sys.argv) == 2:
        main()

        while continue_program:
            continue_program = ask_user_if_continue()
            if not continue_program:
                break

            # Main function prompts a user to input an int to select from pre-made sentences
            main(select_premade_sentence=True)

    while continue_program:
        # Main function prompts a user to input a sentence
        main()

        continue_program = ask_user_if_continue()

    print("Parser exited. Thanks for using!")
