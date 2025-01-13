import os
import sys
# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openai import OpenAI
from agents.job_assistant.agent import JobPositionTipificationAgent
from agents.provider import LlmProvider
import configparser
import pandas as pd
import pandera as pa


def process_col(type:str, content:str) -> str:
    agent = JobPositionTipificationAgent(provider=LlmProvider)
    messages = agent.process(f"""
    {{
        '{type}': '{content}'
    }}
    """)

    # retrieve the last message
    msgs = [msg.strip() for msg in messages[-1].get("content").split(",")]
    return list(msgs)


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '.config'))
api_key = config.get('DEFAULT', 'api_key')
client = OpenAI(api_key=api_key)

LlmProvider = LlmProvider(model='gpt-4o', client=client)

# Read silver data (only 20 rows)
df = pd.read_parquet('s3/silver/real-or-fake-fake-jobposting-prediction.parquet')[0:2]

df['job_responsibilities'] = df.apply(lambda x: process_col('job_responsibilities', x['description']), axis=1)
df['hard_skills'] = df.apply(lambda x: process_col('hard_skills', x['requirements']), axis=1)
df['soft_skills'] = df.apply(lambda x: process_col('soft_skills', x['requirements']), axis=1)

gold_data = df

def validate_list_of_3_strings(series):
    for item in series:
        print(item)
        if len(item) != 3:
            return False
        for string in item:
            if not isinstance(string, str):
                return False
    return True

gold_schema = pa.DataFrameSchema({
    'job_id': pa.Column(pa.Int, nullable=False),
    'title': pa.Column(pa.String, nullable=False),
    'salary_range': pa.Column(pa.String, nullable=True),
    'industry': pa.Column(pa.String, nullable=True),
    'location': pa.Column(pa.String, nullable=True),
    'description': pa.Column(pa.String, nullable=True),
    'requirements': pa.Column(pa.String, nullable=True),
    'required_experience': pa.Column(pa.String, nullable=True),
    'lower_bound_salary': pa.Column(pa.Float, nullable=False),
    'upper_bound_salary': pa.Column(pa.Float, nullable=False),
    'job_responsibilities': pa.Column(object, checks=pa.Check(lambda x: validate_list_of_3_strings(x)), nullable=False),
    'hard_skills': pa.Column(object, checks=pa.Check(lambda x: validate_list_of_3_strings(x)), nullable=False),
    'soft_skills': pa.Column(object, checks=pa.Check(lambda x: validate_list_of_3_strings(x)), nullable=False),
})

try:
    gold_schema.validate(gold_data)
    gold_data.to_parquet('s3/gold/real-or-fake-fake-jobposting-prediction.parquet')
except pa.errors.SchemaError as e:
    print(f"Data validation failed: {e}")
    sys.exit(1)

