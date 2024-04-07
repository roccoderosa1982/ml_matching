
import json

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def check_data(data, has_label=True):
    for item in data:
        if has_label:
            if 'talent' not in item or 'job' not in item or 'label' not in item:
                raise ValueError("Invalid data format. Each item should contain 'talent', 'job', and 'label'.")
            if not isinstance(item['talent'], dict) or not isinstance(item['job'], dict) or not isinstance(item['label'], bool):
                raise ValueError("Invalid data format. 'talent' and 'job' should be dictionaries and 'label' should be a boolean.")
        else:
            if 'talent' not in item or 'job' not in item:
                raise ValueError("Invalid data format. Each item should contain 'talent' and 'job'")    
            if not isinstance(item['talent'], dict) or not isinstance(item['job'], dict):
                raise ValueError("Invalid data format. 'talent' and 'job' should be dictionaries.")

        if 'languages' in item['talent'] and not isinstance(item['talent']['languages'], list):
            raise ValueError("Invalid data format. 'talent.languages' should be a list.")
        if 'languages' in item['job'] and not isinstance(item['job']['languages'], list):
            raise ValueError("Invalid data format. 'job.languages' should be a list.")
        if 'job_roles' in item['talent'] and not isinstance(item['talent']['job_roles'], list):
            raise ValueError("Invalid data format. 'talent.job_roles' should be a list.")
        if 'job_roles' in item['job'] and not isinstance(item['job']['job_roles'], list):
            raise ValueError("Invalid data format. 'job.job_roles' should be a list.")
        if 'seniority' in item['talent'] and not isinstance(item['talent']['seniority'], str):
            raise ValueError("Invalid data format. 'talent.seniority' should be a string.")
        if 'seniorities' in item['job'] and not isinstance(item['job']['seniorities'], list):
            raise ValueError("Invalid data format. 'job.seniorities' should be a list.")
        if 'salary_expectation' in item['talent'] and not isinstance(item['talent']['salary_expectation'], int):
            raise ValueError("Invalid data format. 'talent.salary_expectation' should be an integer.")
        if 'max_salary' in item['job'] and not isinstance(item['job']['max_salary'], int):
            raise ValueError("Invalid data format. 'job.max_salary' should be an integer.")
        if 'min_degree' in item['job'] and not isinstance(item['job']['min_degree'], str):
            raise ValueError("Invalid data format. 'job.min_degree' should be a string.")
        if 'degree' in item['talent'] and not isinstance(item['talent']['degree'], str):
            raise ValueError("Invalid data format. 'talent.degree' should be a string.")

def transform_data(data, has_label=True):
    transformed_data = []
    for item in data:
        talent = item['talent']
        job = item['job']
        if has_label:
            label = item['label']

        # Create a mapping of degree titles to a numerical scale
        degree_scale = {
            "none": 0,
            "apprenticeship":1,
            "bachelor": 2,
            "master": 3,
            "doctorate": 4
        }

        # Create a mapping of language ratings to a numerical scale
        rating_scale = {
            "A1": 1,
            "A2": 2,
            "B1": 3,
            "B2": 4,
            "C1": 5,
            "C2": 6
        }

        # Create a mapping of seniorities to a numerical scale
        seniority_scale = {
            "none": 0,
            "junior": 1,
            "midlevel": 2,
            "senior": 3
        }


        # Transform the talent and job data
        transformed_talent = {
            "degree": degree_scale[talent['degree']],
            "job_roles": talent['job_roles'],
            "seniority": seniority_scale[talent['seniority']],
            "salary_expectation": talent['salary_expectation'],
            "languages": {lang['title']: rating_scale[lang['rating']] for lang in talent['languages']}
        }

        transformed_job = {
            "min_degree": degree_scale[job['min_degree']],
            "job_roles": job['job_roles'],
            "seniorities": [seniority_scale[seniority] for seniority in job['seniorities']],
            "max_salary": job['max_salary'],
            "languages": {lang['title']: rating_scale[lang['rating']] for lang in job['languages'] if lang['must_have']}
        }

        if has_label:
            transformed_data.append((transformed_talent, transformed_job, label)) 
        else:
            transformed_data.append((transformed_talent, transformed_job)) 
    return transformed_data

def heuristic_match(talent: dict, job: dict) -> dict:
    # Check if the talent's degree is equal to or higher than the job's minimum degree
    if talent['degree'] >= job['min_degree']:
        # Check if the talent is interested in at least one of the job roles that the job requires

        if set(talent['job_roles']).intersection(set(job['job_roles'])):
            # Check if the talent speaks at least one of the languages that the job requires, and the talent's level in that language is equal to or higher than the job's required level
            if set(talent['languages'].keys()).intersection(set(job['languages'].keys())) and all(talent['languages'][lang] >= job['languages'][lang] for lang in job['languages'].keys()):
                # Check if the talent's salary expectation is within the job's salary range
                if talent['salary_expectation'] <= job['max_salary']:
                    # Check if the talent's seniority is one of the seniorities that the job allows
                    if talent['seniority'] in job['seniorities']:
                        return True
    return False
