import math
import nltk
import os
from pathlib import Path
import string
import sys

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.data.path.append(os.path.join(Path(__file__).resolve().parent, "nltk_data"))
FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    print("Loading data...")
    # Calculate Inverse Document Frequency (IDF) values across files
    files, file_words, file_idfs = get_file_idfs()
    print("Data loaded.")

    while True:
        # Prompt user for query
        query = set(tokenize(input("Query: ")))

        # Determine top sentence matches
        matches = get_top_sentence_matches(query, files, file_words, file_idfs)

        for match in matches:
            print(match)

        user_input = input("Ask another question? [Y/n]: ")
        if user_input.lower() in ["n", "no"]:
            break

    print("Program exited. Thanks for using!")


def get_file_idfs():
    """
    Load corpus of documents, tokenize all words and compute inverse document frequency (IDF) values.
    """
    # Calculate Inverse Document Frequency (IDF) values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)
    return files, file_words, file_idfs


def get_top_sentence_matches(query, files, file_words, file_idfs):
    """
    Determine top file matches, extract sentences, compute IDF values and then return top sentence matches.
    """
    # Determine top file matches according to Term Frequency - Inverse Document Frequency (TF-IDF) values
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = {}
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    return top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each `.txt` file inside that directory
    to the file's contents as a string.
    """
    files = {}
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), mode="r", encoding="utf8") as file:
            files[filename] = file.read()

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all the words in that document, in order.

    Process document by converting all words to lowercase, and removing any punctuation or English stopwords.
    """
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(document.lower())

    # return filtered words
    return [
        word
        for word in word_tokens
        if word.lower() not in stop_words and word not in string.punctuation
    ]


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list of words,
    return a dictionary that maps words to their Inverse Document Frequency (IDF) values.

    Any word that appears in at least one of the documents should be in the resulting dictionary.
    """
    # Initialize dict to map words to their Inverse Document Frequency (IDF) values
    idfs = {}
    for filename in documents:
        for word in documents[filename]:
            num_docs_with_word = sum(word in documents[filename] for filename in documents)
            idf = math.log(len(documents) / num_docs_with_word)
            idfs[word] = idf

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of files to a list of their words), and
    `idfs` (a dictionary mapping words to their IDF values), return a list of the filenames of the `n` top
    files that match the query, ranked according to Term Frequency - Inverse Document Frequency (tf-idf) values.
    """
    # Calculate sum of TF-IDFs for each file
    tfidfs = {}
    for filename in files:
        file_tfidfs = []
        for word in query:
            term_frequency = files[filename].count(word)
            if word in idfs:
                file_tfidfs.append((word, term_frequency * idfs[word]))

        # Store sum of TF-IDFs for this file in tfidfs dict
        tfidfs[filename] = sum(tfidf for word, tfidf in file_tfidfs)

    # Create sorted list using tfidfs keys, reverse-sorted (i.e. descending order) by corresponding values
    top_matching_files = sorted(tfidfs, key=tfidfs.get, reverse=True)

    # Return `n` top files that match the query
    return top_matching_files[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping sentences to a list of their words),
    and `idfs` (a dictionary mapping words to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should be given to the sentences that have a
    higher query term density.
    """
    # Initialize Boolean flag for checking if at least one word in the query was found in corpus of documents
    word_found = False

    # Calculate matching word measure & query term density for each sentence, storing values inside Sentence class
    sentences_metrics = {}
    for sentence in sentences:
        matching_word_measure = 0
        query_term_count = 0
        for word in query:
            if word in sentences[sentence]:
                word_found = True
                matching_word_measure += idfs[word]
                query_term_count += 1
        query_term_density = query_term_count / len(sentence)
        sentences_metrics[sentence] = Sentence(matching_word_measure, query_term_density)

    if word_found:
        # Create sorted list using sentences_metrics keys, reverse-sorted (i.e. descending order) by values.
        # Sorted by matching word measure, and then by query term density
        top_matching_sentences = sorted(
            sentences_metrics,
            key=lambda s: (sentences_metrics[s].matching_word_measure, sentences_metrics[s].query_term_density),
            reverse=True
        )
    else:
        return ["No matching sentences were found."]

    # Return `n` top sentences that match the query
    return top_matching_sentences[:n]


class Sentence(object):
    def __init__(self, matching_word_measure, query_term_density):
        self.matching_word_measure = matching_word_measure
        self.query_term_density = query_term_density

    def __repr__(self):
        return repr((self.matching_word_measure, self.query_term_density))


if __name__ == "__main__":
    main()
