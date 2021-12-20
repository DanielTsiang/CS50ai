# Answer Bot

### Description

An AI that answers questions.

This chatbot is provided with information relating to artificial intelligence, machine learning, natural language processing, neural networks, probability and Python.

<p align="center">
  <img width="500" src="https://user-images.githubusercontent.com/74436899/146823355-1ba07602-d886-4b1c-9da6-674d58f29dc9.jpeg">
</p>

### Getting Started
1. Visit a demo [here](https://replit.com/@DanielTsiang/answerbot#README.md).
2. Click the green button to run the demo code. Or run ```python answerbot.py corpus``` where ```corpus``` is a directory containing text files.
3. Once the data is loaded, enter your question!
4. A unit test can be run via ```python test_answerbot.py```.

### Example
```
$ python answerbot.py corpus
Query: What are the types of supervised learning?
Types of supervised learning algorithms include Active learning, classification and regression.

$ python answerbot.py corpus
Query: When was Python 3.0 released?
Python 3.0 was released on 3 December 2008.

$ python answerbot.py corpus
Query: How do neurons connect in a neural network?
Neurons of one layer connect only to neurons of the immediately preceding and immediately following layers.
```

### Background
This simple question answering system is based on inverse document frequency (IDF).

The question answering system performs two tasks: document retrieval and passage retrieval. The system will have access to a corpus of text documents. When presented with a query (a question in English asked by the user), document retrieval will first identify which document(s) are most relevant to the query. Once the top documents are found, the top document(s) will be subdivided into passages (in this case, sentences) so that the most relevant passage to the question can be determined.

To find the most relevant documents, term frequency - inverse document frequency i.e. ```tf-idf``` is used to rank documents based both on term frequency for words in the query, and inverse document frequency for words in the query. Once the most relevant documents are found, a combination of inverse document frequency and a query term density measure is used as metrics for scoring passages.

### Technologies Used
* Python with Natural Language Toolkit (NLTK)