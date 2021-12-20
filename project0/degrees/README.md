# Degrees of Separation

### Description
A program that determines how many “degrees of separation” apart two actors are by choosing a sequence of movies that connects them. The program uses a breadth-first search algorithm to find the shortest path from one actor to another.

<p align="center">
  <img width="500" src="https://user-images.githubusercontent.com/74436899/122903111-0120d600-d347-11eb-8398-d63e0e97fd0d.jpg">
</p>

### Getting Started
1. Visit a demo using the small data set [here](https://replit.com/@DanielTsiang/degrees#README.md). To use the large data set, run the code on your local computer.
2. Click the green button to run the demo code. Or run ```python degrees.py large``` to load the large data set.
3. Enter the name of two actors, e.g. Tom Cruise and Tom Hanks.
4. A unit test can be run via ```python test_degrees.py```.

### Example
Example with the large data set loaded:
```
$ python degrees.py large
Loading data...
Data loaded.
Name 1: Emma Watson
Name 2: Jennifer Lawrence
3 degrees of separation.
1: Emma Watson and Brendan Gleeson starred in Harry Potter and the Order of the Phoenix
2: Brendan Gleeson and Michael Fassbender starred in Trespass Against Us
3: Michael Fassbender and Jennifer Lawrence starred in X-Men: First Class
```

### Technologies Used
* Python
