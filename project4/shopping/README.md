# Shopping

### Description
An AI that predicts whether online shopping customers will complete a purchase, by using a nearest-neighbor classifier.

<p align="center">
  <img width="500" src="https://user-images.githubusercontent.com/74436899/146847921-a4ce2602-363a-4c06-8d4f-0dc4b2e8a0d5.png">
</p>

### Getting Started
1. Visit a demo [here](https://replit.com/@DanielTsiang/shopping#README.md).
2. Click the green button to run the demo code. Or run ```python shopping.py shopping.csv```.
3. A unit test can be run via ```python test_shopping.py ```.

### Example
```
$ python shopping.py shopping.csv
Correct: 4088
Incorrect: 844
True Positive Rate: 41.02%
True Negative Rate: 90.55%
```

### Background
Given information about a user — how many pages they’ve visited, whether they’re shopping on a weekend, what web browser they’re using, etc. — the nearest-neighbor classifier will predict whether the user will make a purchase.

To train the classifier, shopping.csv contains data from a shopping website from about 12,000 users sessions.

Two values are measured:
* sensitivity (also known as the “true positive rate”)
* specificity (also known as the “true negative rate”).

Sensitivity refers to the proportion of positive examples that were correctly identified: in other words, the proportion of users who did go through with a purchase who were correctly identified.

Specificity refers to the proportion of negative examples that were correctly identified: in this case, the proportion of users who did not go through with a purchase who were correctly identified.

The goal is to build a classifier that performs reasonably on both metrics.

### Technologies Used
* Python
