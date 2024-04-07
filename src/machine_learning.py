
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsRestClassifier
import numpy as np
import joblib


def min_max_normalize_to_A_B(X, MIN, MAX, A, B):
    """
    Normalize to [A,B] the input array X using min-max normalization.
    """

     # Normalize the values to the interval [A, B]
    return A + (X - MIN) * (B - A) / (MAX - MIN)


def logistic_cdf(x, mu, s):
    """
    Calculate the logistic cumulative distribution function (CDF).

    Parameters:
    x (float or array-like): The point(s) at which to evaluate the CDF.
    mu (float): The location parameter of the distribution.
    s (float): The scale parameter of the distribution.

    Returns:
    float or ndarray: The value(s) of the logistic CDF at the given point(s).
    """
    return 1 / (1 + np.exp(-(x - mu) / s))


def salary_match_score(expected_salary,max_salary):
    """
    Calculate heuristic salary match score using logistic cumulative distribution function (CDF).

    Parameters:
    expected_salary (float): The point(s) at which to evaluate the CDF.
    expected_salary (float): The location parameter of the distribution.


    Returns:
    float : match score.
    """

    #parameters are arbitrary here
    normalised_diff = min_max_normalize_to_A_B(min(max_salary-expected_salary,0), -50000, 0, 0, 3)

    return logistic_cdf(normalised_diff, 1, 0.32)

def extract_features(talent, job):
    feature_vector = []

    # Degree
    feature_vector.append(talent['degree'])
    feature_vector.append(job['min_degree'])
    feature_vector.append(talent['degree'] >= job['min_degree']) #match

    # Seniority
    feature_vector.append(talent['seniority'])
    feature_vector.append(min(job['seniorities']))
    feature_vector.append(max(job['seniorities']))
    feature_vector.append(talent['seniority'] in job['seniorities']) #match

    # Salary Expectation
    feature_vector.append(talent['salary_expectation'])
    feature_vector.append(job['max_salary'])
    feature_vector.append(talent['salary_expectation'] <= job['max_salary']) #match
    feature_vector.append(salary_match_score(talent['salary_expectation'], job['max_salary'])) #match score

    # Languages
    talent_langs = set(talent['languages'].keys())
    job_langs = set(job['languages'].keys())
    common_langs = talent_langs.intersection(job_langs)
    lang_match = all(talent['languages'].get(lang, 0) >= job['languages'].get(lang, 0) for lang in common_langs)
    feature_vector.append(int(bool(common_langs and lang_match))) #match

    # Job roles
    feature_vector.append(int(bool(set(talent['job_roles']).intersection(set(job['job_roles']))))) #match

    return feature_vector

def generate_dataset(transformed_data):
    # Initialize lists to hold the features and labels
    features = []
    labels = []

    # Iterate over the transformed data
    for talent, job, label in transformed_data:
        # Extract features for this row
        feature_vector = extract_features(talent, job)

        # Append the feature vector and label to the dataset
        features.append(feature_vector)
        labels.append(label)

    # Convert the lists to numpy arrays
    features = np.array(features, dtype=float)
    labels = np.array(labels)

    return features, labels

def generate_inference_dataset(transformed_data):
    # Initialize lists to hold the features and labels
    features = []

    # Iterate over the transformed data
    for talent, job in transformed_data:
        # Extract features for this row
        feature_vector = extract_features(talent, job)

        # Append the feature vector and label to the dataset
        features.append(feature_vector)

    # Convert the lists to numpy arrays
    features = np.array(features, dtype=float)

    return features



def train_and_evaluate_model(transformed_data):

    features, labels = generate_dataset(transformed_data)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    # Train a Decision Tree Classifier
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train) 

    # Make predictions on the test set
    y_pred = clf.predict(X_test)

    # Evaluate the model
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))
    
    return clf

def predict_match(clf, transformed_data):
    features = generate_inference_dataset(transformed_data)
    y_pred = clf.predict(features)
    y_score = clf.predict_proba(features)
    return y_pred,y_score
    

def save_trained_model(model, model_path):
    joblib.dump(model, model_path) 
    
def load_trained_model(model_path):
    model = joblib.load(model_path)
    return model
    