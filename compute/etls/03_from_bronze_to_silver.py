import pandas as pd
import pandera as pa

df = pd.read_csv("s3/bronze/real-or-fake-fake-jobposting-prediction.csv")

# select columns job_id, title, salary_range, industry, location, description, requirements, required_experience
silver_df = df[['job_id', 'title', 'salary_range', 'industry', 'location', 'description', 'requirements', 'required_experience']]

# create two new columns lower_bound_salary and upper_bound_salary from salary_range using pandas and panderas for schema validation
splitted_df = (
    silver_df
    .fillna({'salary_range': '0-0'})
    .assign(
        lower_bound_salary=lambda x: x['salary_range'].str.split('-').str[0].astype(str),
        upper_bound_salary=lambda x: x['salary_range'].str.split('-').str[1].astype(str)
    ) 
)

# some lower_bound_salary and upper_bound_salary are not numbers, they have values like 'Oct' and 'Sep', ignore those rows
silver_df = (
    splitted_df
    .loc[lambda x: x['lower_bound_salary'].str.isnumeric()]
    .loc[lambda x: x['upper_bound_salary'].str.isnumeric()]
    .astype({
        'lower_bound_salary': float,
        'upper_bound_salary': float
    })
)

# Schema validation

silver_schema = pa.DataFrameSchema({
    'job_id': pa.Column(pa.Int, nullable=False),
    'title': pa.Column(pa.String, nullable=False),
    'salary_range': pa.Column(pa.String, nullable=True),
    'industry': pa.Column(pa.String, nullable=True),
    'location': pa.Column(pa.String, nullable=True),
    'description': pa.Column(pa.String, nullable=True),
    'requirements': pa.Column(pa.String, nullable=True),
    'required_experience': pa.Column(pa.String, nullable=True),
    'lower_bound_salary': pa.Column(pa.Float, checks=[
        pa.Check.greater_than_or_equal_to(0),
        pa.Check.less_than(1_000_000_000)
    ], nullable=False),
    'upper_bound_salary': pa.Column(pa.Float, nullable=False),
})

try:
    silver_schema.validate(silver_df)
except pa.errors.SchemaError as e:
    print("Schema errors and failure cases")
    df_error_cases = e.failure_cases
    print("\nDataFrame object that failed validation")
    df_error_data = e.data

    # save error cases to a file
    df_error_cases.to_csv("s3/silver/silver_schema_errors.csv", index=False)

# save silver_df to s3
silver_df.to_parquet('./s3/silver/real-or-fake-fake-jobposting-prediction.parquet', index=False)