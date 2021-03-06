# Heredity

### Description
An AI that assesses the likelihood that a person will have a particular genetic trait. Relationships are modelled by forming a Bayesian Network of each person's ```Gene``` and ```Trait``` random variables.

 A Bayesian Network model is used to make inferences about a population. Given information about people, who their parents are, and whether they have a particular observable trait (e.g. hearing loss) caused by a given gene, the AI will infer the probability distribution for each person’s genes, as well as the probability distribution for whether any person will exhibit the trait in question.

<p align="center">
  <img width="500" src="https://user-images.githubusercontent.com/74436899/125932475-d4479b68-644a-4bf1-b38e-87b90d5b1ceb.png">
</p>

### Getting Started
1. Visit a demo [here](https://replit.com/@DanielTsiang/heredity#README.md).
2. Click the green button to run the demo code for the ```family0``` data set.
3. Alternatively run ```python heredity.py data/family1.csv``` or ```python heredity.py data/family2.csv``` to calculate the genetic probabilities for other data sets.
4. Unit tests for all 3 data sets can be run via ```python test_heredity.py```.

### Example
Example with the ```family0``` data set:
```
$ python heredity.py data/family0.csv
Harry:
  Gene:
    2: 0.0092
    1: 0.4557
    0: 0.5351
  Trait:
    True: 0.2665
    False: 0.7335
James:
  Gene:
    2: 0.1976
    1: 0.5106
    0: 0.2918
  Trait:
    True: 1.0000
    False: 0.0000
Lily:
  Gene:
    2: 0.0036
    1: 0.0136
    0: 0.9827
  Trait:
    True: 0.0000
    False: 1.0000
```

### Background
Mutated versions of the GJB2 gene are one of the leading causes of hearing impairment in newborns. Each person carries two versions of the gene, so each person has the potential to possess either 0, 1, or 2 copies of the hearing impairment version GJB2. Unless a person undergoes genetic testing, though, it’s not so easy to know how many copies of mutated GJB2 a person has. This is some “hidden state”: information that has an effect that we can observe (hearing impairment), but that we don’t necessarily directly know. After all, some people might have 1 or 2 copies of mutated GJB2 but not exhibit hearing impairment, while others might have no copies of mutated GJB2 yet still exhibit hearing impairment.

Every child inherits one copy of the GJB2 gene from each of their parents. If a parent has two copies of the mutated gene, then they will pass the mutated gene on to the child; if a parent has no copies of the mutated gene, then they will not pass the mutated gene on to the child; and if a parent has one copy of the mutated gene, then the gene is passed on to the child with probability 0.5. After a gene is passed on, though, it has some probability of undergoing additional mutation: changing from a version of the gene that causes hearing impairment to a version that does not, or vice versa.

We can attempt to model all of these relationships by forming a Bayesian Network of all the relevant variables, as in the one below, which considers a family of two parents and a single child.

<p align="center">
  <img width="500" src="https://user-images.githubusercontent.com/74436899/125946530-30e96c89-01f2-4da0-9336-07237c5e54c3.png">
</p>

Each person in the family has a ```Gene``` random variable representing how many copies of a particular gene (e.g., the hearing impairment version of GJB2) a person has: a value that is 0, 1, or 2. Each person in the family also has a ```Trait``` random variable, which is ```yes``` or ```no``` depending on whether that person expresses a trait (e.g., hearing impairment) based on that gene. There’s an arrow from each person’s ```Gene``` variable to their ```Trait``` variable to encode the idea that a person’s genes affect the probability that they have a particular trait. Meanwhile, there’s also an arrow from both the mother and father’s ```Gene``` random variable to their child’s ```Gene``` random variable: the child’s genes are dependent on the genes of their parents.

### Technologies Used
* Python