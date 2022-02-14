import calendar
import csv
import numpy as np
import sys

from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler

CROSS_VALIDATION_SIZE = 5
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    print("Predicting labels...")
    y_test, y_pred = predict_labels()

    # Evaluate model performance
    report = classification_report(y_test, y_pred, output_dict=True)

    # Extract results
    print("Results:")
    # `accuracy` represents the proportion of labels that were accurately identified
    print(f"Accuracy: {100 * report['accuracy']:.1f}%")

    # `sensitivity` represents the "true positive rate":
    # the proportion of actual positive labels that were accurately identified.
    print(f"True Positive Rate: {100 * report['1']['recall']:.1f}%")

    # `specificity` represents the "true negative rate":
    # the proportion of actual negative labels that were accurately identified.
    print(f"True Negative Rate: {100 * report['0']['recall']:.1f}%")

    # Show full classification report
    print(f"Classification report:\n {classification_report(y_test, y_pred)}")


def predict_labels() -> tuple[list, list]:
    """
    Load and split data into train and test sets.
    Tune and train model, then use it to make predictions on label classification.
    """
    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE, random_state=42, stratify=labels
    )

    # Tune and train model, and use it to make predictions
    model = train_model(X_train, y_train)
    y_pred = model.predict(X_test)

    return y_test, y_pred


def train_model(X_train: list, y_train: list) -> GridSearchCV:
    """
    Given a list of evidence lists (X_train) and a list of labels (y_train),
    return a fitted k-nearest neighbor model, with a tuned value of k, trained on the data.
    """
    # Create pipeline
    pipeline = Pipeline([("scaler", RobustScaler()),
                         ("knn", KNeighborsClassifier())])

    # Create hyperparameter grid
    params = {"knn__n_neighbors": np.arange(5, 12)}

    # Use cross-fold validation to tune k-nearest neighbor model, and then fit the model
    model_cross_validation = GridSearchCV(pipeline, params, cv=CROSS_VALIDATION_SIZE)
    model_cross_validation.fit(X_train, y_train)

    # Return fitted model
    return model_cross_validation


def load_data(filename: str) -> tuple[list, list]:
    """
    Load shopping data from a CSV file `filename` and convert into a list of evidence lists and a list of labels.
    Return a tuple (evidence, labels).

    `evidence` should be a list of lists, where each list contains the following values, in order:
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

    labels should be the corresponding list of labels, where each label is 1 if Revenue is true, and 0 otherwise.
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
                int(row[14]),   # TrafficType
                1 if row[15] == "Returning_Visitor" else 0,  # VisitorType
                int(row[16] == "TRUE")  # Weekend
            ])

            labels.append(
                int(row[17] == "TRUE")  # Revenue
            )

    return evidence, labels


if __name__ == "__main__":
    main()
