# Match Job and Talents with ML

This is a Python project for matching talents to jobs using machine learning.

## Job-Talent Matching Algorithm
The provided code is used to match job seekers (talents) with job postings (jobs). The code reads a JSON file containing talent and job data, validates the data format, transforms the data into a format suitable for matching, and then matches the talents to the jobs using a heuristic-based matching algorithm and a more sophisticated machine learning solution.

### Heuristic Algorithm
The heuristic algorithm used in this code is a simple matching algorithm that checks if the talent's degree is equal to or higher than the job's minimum degree, if the talent is interested in at least one of the job roles that the job requires, and if the talent speaks at least one of the languages that the job requires. The algorithm also checks if the talent's seniority level is within the range of seniorities required by the job.

### Machine Learning Model
In addition to the heuristic algorithm, a machine learning model is used in the match_bulk function. This model is trained on historical data to predict whether a talent is a good match for a job. The model takes into account various features such as the degree of the talent, the job roles they're interested in, the languages they speak, and the seniority level.

The match_bulk function prepares the data for the model and uses the model to predict the match for each talent-job pair. The model's predictions are then returned along with the talent and job data.

Note: The example dataset is very easy to learn, indeed both heuristic and ML model get very high accuracy.

## Installation

1. Clone the repository:

```console
bash
git clone https://github.com/yourusername/your-repo.git](https://github.com/roccoderosa1982/ml_matching.git
cd your-repo
```


2. Create a virtual environment and install the dependencies:

```console
bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
pip install -r requirements.txt
```


## Usage

To run the project, use the following command:

```console
bash
python main.py
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
