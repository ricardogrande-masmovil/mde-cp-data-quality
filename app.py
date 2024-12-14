import kagglehub

# Download latest version
path = kagglehub.dataset_download("shivamb/real-or-fake-fake-jobposting-prediction", path="/Users/ricardo/Documents/MBIT/mde-m05-pc-data-quality/s3/raw")

print("Path to dataset files:", path)