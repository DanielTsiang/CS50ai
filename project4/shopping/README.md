# Shopping

### Description
An AI that predicts whether online shopping customers will complete a purchase,
by using a tuned nearest-neighbor classifier on a scaled dataset.

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
Accuracy: 88.6%
True Positive Rate: 52.0%
True Negative Rate: 95.3%
Classification metrics:
               precision    recall  f1-score   support

           0       0.92      0.95      0.93      4169
           1       0.67      0.52      0.59       763

    accuracy                           0.89      4932
   macro avg       0.79      0.74      0.76      4932
weighted avg       0.88      0.89      0.88      4932
```

### Background
Given information about a user — how many pages they’ve visited, whether they’re shopping on a weekend,
what web browser they’re using, etc. — the nearest-neighbor classifier will predict whether the user will make a purchase.
The number of nearest-neighbors used (i.e. the k-value) is tuned, to improve the performance of the classifier.

To train the classifier, shopping.csv contains data from a shopping website from about 12,000 users sessions.
The dataset is scaled using statistics that are robust to outliers, thus further improving the model's prediction performance.

Three values are highlighted in the results:
* accuracy (i.e. the correct predictions)
* sensitivity (also known as the “true positive rate”)
* specificity (also known as the “true negative rate”).

Sensitivity refers to the proportion of positive examples that were correctly identified: in other words, the proportion of users who did go through with a purchase who were correctly identified.

Specificity refers to the proportion of negative examples that were correctly identified: in this case, the proportion of users who did not go through with a purchase who were correctly identified.

The goal is to build a classifier that performs reasonably on the classification metrics.

### Technologies Used
* Python
