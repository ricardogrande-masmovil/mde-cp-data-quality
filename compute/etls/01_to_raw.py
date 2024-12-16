import requests
import os

url = "https://www.kaggle.com/api/v1/datasets/download/shivamb/real-or-fake-fake-jobposting-prediction"
output_file = "real-or-fake-fake-jobposting-prediction.zip"
output_dir = 's3/raw'

os.makedirs(output_dir, exist_ok=True)
response = requests.get(url, allow_redirects=True)
file_path = os.path.join(output_dir, output_file)
with open(file_path, 'wb') as file:
	file.write(response.content)
	print(f"Downloaded file saved as {file_path}")