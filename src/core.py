from .datasets import load_and_transform_train_data, load_and_transform_test_data, transform_test_data
from .machine_learning import train_and_evaluate_model,save_trained_model, load_trained_model, predict_match



def train_model(file_path): 
    transformed_data = load_and_transform_train_data(file_path)
    return train_and_evaluate_model(transformed_data)

def save_model(model, model_path):
    save_trained_model(model, model_path)
    
def load_model(model_path):
    model = load_trained_model(model_path)
    return model

def batch_predict_match(model, file_path):
    transformed_data = load_and_transform_test_data(file_path)
    result = predict_match(model, transformed_data)
    return result

def batch_predict_match(model, batch_data):
    transformed_data = transform_test_data(batch_data)
    labels, score = predict_match(model, transformed_data)
    return labels, score[:,1]
    
def single_predict_match(model, rec):
    transformed_data = transform_test_data([rec])
    labels, score = predict_match(model, transformed_data)
    return labels[0], score[0][1]