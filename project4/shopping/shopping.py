import calendar
import csv
import numpy as np
import sys

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier

CROSS_VALIDATION_SIZE = 5
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    untuned_results, tuned_results = find_predictions()

    # Get number of correctly and incorrectly classified samples
    correct_untuned = accuracy_score(untuned_results["y_test"], untuned_results["predictions"], normalize=False)
    incorrect_untuned = len(untuned_results["predictions"]) - correct_untuned

    correct_tuned = accuracy_score(tuned_results["y_test"], tuned_results["predictions"], normalize=False)
    incorrect_tuned = len(tuned_results["predictions"]) - correct_tuned

    # Get confusion matrix and classification report
    confusion_matrix_untuned = confusion_matrix(untuned_results["y_test"], untuned_results["predictions"])
    classification_report_untuned = classification_report(untuned_results["y_test"], untuned_results["predictions"])

    confusion_matrix_tuned = confusion_matrix(tuned_results["y_test"], tuned_results["predictions"])
    classification_report_tuned = classification_report(tuned_results["y_test"], tuned_results["predictions"])

    # Print results
    print("Untuned results:")
    print(f"Correct: {correct_untuned}")
    print(f"Incorrect: {incorrect_untuned}")
    print(f"True Positive Rate: {100 * untuned_results['sensitivity']:.2f}%")
    print(f"True Negative Rate: {100 * untuned_results['specificity']:.2f}%")
    print(f"Confusion matrix:\n {confusion_matrix_untuned}")
    print(f"Classification report:\n {classification_report_untuned}")

    print("-------------------------------------------------")
    print("Tuned results:")
    print(f"Correct: {correct_tuned}")
    print(f"Incorrect: {incorrect_tuned}")
    print(f"True Positive Rate: {100 * tuned_results['sensitivity']:.2f}%")
    print(f"True Negative Rate: {100 * tuned_results['specificity']:.2f}%")
    print(f"Confusion matrix:\n {confusion_matrix_tuned}")
    print(f"Classification report:\n {classification_report_tuned}")


def find_predictions():
    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE, random_state=42, stratify=labels
    )

    # Train model and make predictions
    model_untuned, model_tuned = train_model(X_train, y_train)

    predictions_untuned = model_untuned.predict(X_test)
    predictions_tuned = model_tuned.predict(X_test)

    sensitivity_untuned, specificity_untuned = evaluate(y_test, predictions_untuned)
    sensitivity_tuned, specificity_tuned = evaluate(y_test, predictions_tuned)

    untuned_results = {
        "y_test": y_test,
        "predictions": predictions_untuned,
        "sensitivity": sensitivity_untuned,
        "specificity": specificity_untuned
    }

    tuned_results = {
        "y_test": y_test,
        "predictions": predictions_tuned,
        "sensitivity": sensitivity_tuned,
        "specificity": specificity_tuned
    }

    return untuned_results, tuned_results


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence, labels = [], []

    # Create month abbreviation to number mapping
    month_to_number = {month: index - 1 for index, month in enumerate(calendar.month_abbr) if month}

    # Read data in from file
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            evidence.append([
                int(row[0]),    # Administrative
                float(row[1]),  # Administrative_Duration
                int(row[2]),    # Informational
                float(row[3]),  # Informational_Duration
                int(row[4]),    # ProductRelated
                float(row[5]),  # ProductRelated_Duration
                float(row[6]),  # BounceRates
                float(row[7]),  # ExitRates
                float(row[8]),  # PageValues
                float(row[9]),  # SpecialDay
                month_to_number[row[10][:3]],  # Month
                int(row[11]),   # OperatingSystems
                int(row[12]),   # Browser
                int(row[13]),   # Region
                int(row[14]),   # TrafficTyp
                1 if row[15] == "Returning_Visitor" else 0,  # VisitorType
                int(row[16] == "TRUE")  # Weekend
            ])

            labels.append(
                int(row[17] == "TRUE")  # Revenue
            )

    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Instantiate model
    model_untuned = KNeighborsClassifier(n_neighbors=1)

    # Tune hyperparameter
    model_tuned = tuning(model_untuned, evidence, labels)

    # Fit untuned model
    model_untuned.fit(evidence, labels)

    # Return fitted model
    return model_untuned, model_tuned


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity, specificity = 0.0, 0.0
    positive, negative = 0.0, 0.0

    for label, prediction in zip(labels, predictions):
        if label == 1:  # if label is positive, then we calculate sensitivity (positive rate)
            positive += 1
            if label == prediction:
                sensitivity += 1

        else:  # if label is negative, then we calculate specificity (negative rate)
            negative += 1
            if label == prediction:
                specificity += 1

    sensitivity /= positive
    specificity /= negative

    return sensitivity, specificity


def tuning(model, X_train, y_train):
    # Create hyperparameter grid
    hyperparameter_grid = {"n_neighbors": np.arange(1, 16)}
    model_cross_validation = GridSearchCV(model, hyperparameter_grid, cv=CROSS_VALIDATION_SIZE)
    model_cross_validation.fit(X_train, y_train)

    # Return tuned KNN parameter
    return model_cross_validation


if __name__ == "__main__":
    main()
