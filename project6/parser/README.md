# Parser

### Description

An AI that parses sentences and extracts noun phrases.

<p align="center">
  <img width="500" src="https://user-images.githubusercontent.com/74436899/146602265-1d2477ae-95bd-4b29-a5dc-94cb400ebe21.png">
</p>

### Getting Started
1. Visit a demo [here](https://replit.com/@DanielTsiang/parser#README.md).
2. Click the green button to run the demo code. Or run ```python sentence_parser.py [sentences/<number>.txt]```.
3. Optionally, a path to a text file containing a sentence can be given. The sentences folder contains pre-made sentences using words that the AI can understand.
4. If no text file path is given, the user can enter their own sentence constructed using the words defined in the variable ```TERMINALS``` on line 6.
5. A unit test can be run via ```python test_sentence_parser.py```.

### Example
```
$ python sentence_parser.py sentences/7.txt
Sentence: She never said a word until we were at the door here.
Tree:
                                  S                                     
            ______________________|_____________                         
           |                      |             S                       
           |                      |     ________|_______                 
           S                      |    |                VP              
  _________|____                  |    |             ___|____________    
 |              VP                |    |            VP               |  
 |     _________|___              |    |    ________|___             |   
 |    |             VP            |    |   |            PP           |  
 |    |     ________|___          |    |   |     _______|___         |   
 NP   |    |            NP        |    NP  |    |           NP       |  
 |    |    |         ___|___      |    |   |    |        ___|___     |   
 N   Adv   V       Det      N    Conj  N   V    P      Det      N   Adv 
 |    |    |        |       |     |    |   |    |       |       |    |   
she never said      a      word until  we were  at     the     door here

Noun Phrase Chunks:
    she
    a word
    we
    the door
```

### Background
Context-free grammar formalism is used to parse English sentences and determine their structure. In context-free grammar, rewriting rules are repeatedly applied to transform symbols into other symbols. The objective is to start with a non-terminal symbol ```S``` (representing a sentence) and repeatedly apply context-free grammar rules until a complete sentence of terminal symbols (i.e., words) is generated. 

The rule ```S -> N V```, for example, means that the ```S``` symbol can be rewritten as ```N V``` (a noun followed by a verb). If there is also the rule ```N -> "Holmes"``` and the rule ```V -> "sat"```, the complete sentence ```"Holmes sat."``` can be generated.

More complex rules are required to account for more complex types of sentences. E.g. the grammar above would need to be modified further to account for phrases such as noun phrases.

### Technologies Used
* Python with Natural Language Toolkit (NLTK)