# PageRank

### Description
An AI that ranks web pages by importance.

Two approaches are used for calculating PageRank:
1. Sampling pages from a Markov Chain random surfer.
2. Iteratively applying the PageRank formula.

<p align="center">
  <img width="500" src="https://user-images.githubusercontent.com/74436899/125453255-1a46730d-c7d9-49df-a6d2-33854a48bf7e.png">
</p>

### Getting Started
1. Visit a demo [here](https://replit.com/@DanielTsiang/pagerank#README.md).
2. Click the green button to run the demo code for the ```corpus0``` data set.
3. Alternatively run ```python pagerank.py corpus1``` or ```python pagerank.py corpus2``` to calculate PageRank for other data sets.
4. Unit tests for the two approaches can be run via ```python test_pagerank.py```.

### Example
Example with the ```corpus0``` data set:
```
$ python pagerank.py corpus0
PageRank Results from Sampling (n = 10000)
  1.html: 0.2216
  2.html: 0.4271
  3.html: 0.2169
  4.html: 0.1344

PageRank values stable after 11 iterations.
PageRank Results from Iteration
  1.html: 0.2198
  2.html: 0.4294
  3.html: 0.2198
  4.html: 0.1311
```

### Background
When search engines like Google display search results, they do so by placing more “important” and higher-quality pages higher in the search results than less important pages.

The PageRank algorithm was created by Google’s co-founders. In PageRank’s algorithm, a website is more important if it is linked to by other important websites, and links from less important websites have their links weighted less. Thus, each page is given a rank according to the number of incoming links it has from other important pages, and higher ranks signal higher importance.

#### Random Surfer Model
One strategy to calculate PageRank is with the random surfer model, which considers the behavior of a hypothetical surfer on the internet who clicks on links at random. A page’s PageRank can then be described as the probability that a random surfer is on that page at any given time.  

By sampling states randomly from the Markov Chain, we can get an estimate for each page’s PageRank. We can start by choosing a page at random, then keep following links at random, keeping track of how many times we’ve visited each page. After we’ve gathered all of our samples (based on a number we choose in advance), the proportion of the time we were on each page can give an estimate for that page’s rank. To ensure we can always get to somewhere else in the corpus of web pages, a damping factor is used.

#### Iterative Algorithm
A page’s PageRank can be defined using a recursive mathematical expression.

There are two ways that a random surfer could end up on the page:
1. With probability ```1 - d```, the surfer chose a page at random and ended up on page ```p```.
2. With probability ```d```, the surfer followed a link from a page ```i``` to page ```p```.

<p align="left">
  <img width="500" src="https://user-images.githubusercontent.com/74436899/125455676-e8d08756-70f0-4496-9671-a7b9db712d80.png">
</p>

In this formula, ```d``` is the damping factor, ```N``` is the total number of pages in the corpus, ```i``` ranges over all pages that link to page ```p```, and ```NumLinks(i)``` is the number of links present on page ```i```.

The PageRank values for each page can be calculated via iteration: 
1. Start by assuming the PageRank of every page is ```1 / N``` (i.e., equally likely to be on any page). 
2. Use the above formula to calculate new PageRank values for each page, based on the previous PageRank values. 
3. If we keep repeating this process, calculating a new set of PageRank values for each page based on the previous set of PageRank values, eventually the PageRank values will converge (i.e., not change by more than a small threshold with each iteration).

### Technologies Used
* Python
