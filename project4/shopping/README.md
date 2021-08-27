# Shopping

### Description
An AI that predicts whether online shopping customers will complete a purchase, by using a nearest-neighbor classifier.

<p align="center">
  <img width="500" src="https://user-images.githubusercontent.com/74436899/131148662-6eb5ff59-d496-44a2-90d6-490c39d7da4d.png">
</p>

### Example
```
$ python shopping.py shopping.csv
Correct: 4088
Incorrect: 844
True Positive Rate: 41.02%
True Negative Rate: 90.55%
```

### Background
Given information about a user — how many pages they’ve visited, whether they’re shopping on a weekend, what web browser they’re using, etc. — the nearest-neighbor classifier will predict whether or not the user will make a purchase. 

To train the classifier, shopping.csv contains data from a shopping website from about 12,000 users sessions.

Two values are measured:
* sensitivity (also known as the “true positive rate”)
* specificity (also known as the “true negative rate”).

Sensitivity refers to the proportion of positive examples that were correctly identified: in other words, the proportion of users who did go through with a purchase who were correctly identified.

Specificity refers to the proportion of negative examples that were correctly identified: in this case, the proportion of users who did not go through with a purchase who were correctly identified. 

The goal is to build a classifier that performs reasonably on both metrics.

### Technologies Used
* Python