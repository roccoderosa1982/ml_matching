from src.core import train_model, save_model


def train_and_save_model(data_file, model_file):
    clf = train_model(data_file)
    save_model(clf, model_file)
    
    
if __name__ == "__main__":
    train_and_save_model('data/data.json', 'model/model.joblib')