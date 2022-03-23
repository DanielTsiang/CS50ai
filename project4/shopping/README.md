# Shopping

### Description
An AI that predicts whether online shopping customers will complete a purchase,
by using a tuned nearest-neighbor classifier on an overbalanced and scaled data set.

Feature engineering was performed to select the best features with the highest scores.

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
Accuracy: 84.8%
True Positive Rate: 77.9%
True Negative Rate: 86.1%
Classification metrics:
               precision    recall  f1-score   support
               
           0       0.96      0.86      0.91      4169
           1       0.51      0.78      0.61       763
           
    accuracy                           0.85      4932
   macro avg       0.73      0.82      0.76      4932
weighted avg       0.89      0.85      0.86      4932
```

### Background
Given information about a user — how many pages they’ve visited, whether they’re shopping on a weekend,
what web browser they’re using, etc. — the nearest-neighbor classifier will predict whether the user will make a purchase.
The number of features and nearest-neighbors used (i.e. k-values) were tuned, via cross-validated grid search, to improve the performance of the classifier.

To train the classifier, shopping.csv contains data from a shopping website from about 12,000 users sessions.
Since the data is imbalanced, Synthetic Minority Oversampling Technique (SMOTE) is used to create oversampled training data.
The data set is also scaled using statistics that are robust to outliers, thus further improving the model's prediction performance.

Three values are highlighted in the results:
* accuracy (i.e. the correct predictions)
* sensitivity (also known as the “true positive rate”)
* specificity (also known as the “true negative rate”).

Sensitivity refers to the proportion of positive examples that were correctly identified: in other words, the proportion of users who did go through with a purchase who were correctly identified.

Specificity refers to the proportion of negative examples that were correctly identified: in this case, the proportion of users who did not go through with a purchase who were correctly identified.

The goal is to build a classifier that performs reasonably on the classification metrics.

### Technologies Used
* Python
