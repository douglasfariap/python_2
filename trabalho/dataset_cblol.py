import kagglehub

# Download latest version
path = kagglehub.dataset_download("arthur1511/lol-esports-2022")

print("Path to dataset files:", path)