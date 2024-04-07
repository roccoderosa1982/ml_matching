
from .utils import load_data, check_data, transform_data

def load_and_transform_train_data(file_path):
    data = load_data(file_path)
    check_data(data, has_label=True)
    transformed_data = transform_data(data, has_label=True)
    return transformed_data

def load_and_transform_test_data(file_path):
    data = load_data(file_path)
    check_data(data, has_label=False)
    transformed_data = transform_data(data, has_label=False)
    return transformed_data

def transform_test_data(data):
    check_data(data, has_label=False)
    transformed_data = transform_data(data, has_label=False)
    return transformed_data
