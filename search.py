from src.core import load_model, batch_predict_match, single_predict_match
from src.utils import load_data
import json

class Search:
    def __init__(self, model_path) -> None:
        self.model = load_model(model_path)

    def match(self, talent: dict, job: dict) -> dict:
        # ==> Method description <==
        # This method takes a talent and job as input and uses the machine learning
        # model to predict the label. Together with a calculated score, the dictionary
        # returned has the following schema:
        #
        # {
        #   "talent": ...,
        #   "job": ...,
        #   "label": ...,
        #   "score": ...
        # }
        #
        data = {'talent':talent, 'job':job}
        label, score = single_predict_match(self.model, data)
        
        res = {
            'talent':talent,
            'job':job,
            'label':label,
            'score':score
        
        }
        
        return res
        

    def match_bulk(self, talents: list, jobs: list) -> list:
        # ==> Method description <==
        # This method takes a multiple talents and jobs as input and uses the machine
        # learning model to predict the label for each combination. Together with a
        # calculated score, the list returned (sorted descending by score!) has the
        # following schema:
        #
        # [
        #   {
        #     "talent": ...,
        #     "job": ...,
        #     "label": ...,
        #     "score": ...
        #   },
        #   {
        #     "talent": ...,
        #     "job": ...,
        #     "label": ...,
        #     "score": ...
        #   },
        #   ...
        # ]
        #
        data = []
        for t,j in zip(talents,jobs):
            data_rec = {'talent':t, 'job':j}
            data.append(data_rec)
        labels, scores = batch_predict_match(self.model, data)
        
        res = [{'talent':t,'job':j,'label':l,'score':s} for t,j,l,s in zip(talents,jobs,labels,scores)]
        return res

    
def search_main():
    
    model = 'model/model.joblib'
    single_talent = load_data('data/single_talent.json')
    single_job = load_data('data/single_job.json')
    
    talents = load_data('data/list_talents.json')
    jobs = load_data('data/list_jobs.json')
    
    sr = Search(model)
    print("\n\nTesting single match...")
    print(sr.match(single_talent, single_job))
    
    print("\n\nTesting batch match,showing only top 5 result...")
    print(sr.match_bulk(talents, jobs)[:5])

if __name__ == "__main__":
    
    sarch_main()
    
    
    
    
 