from train_model import train_and_save_model
from search import search_main

if __name__ == "__main__":
    
    train_and_save_model('data/data.json', 'model/model.joblib')
    search_main()
    