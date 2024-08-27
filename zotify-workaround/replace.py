import json
import os
from pathlib import Path

# Define the input and output paths
input_path = 'credentials.json'  # Assuming the script runs in the same directory as the credentials.json file
output_path = Path.home() / '.local/share/zotify/credentials.json'

# Load the JSON data from the input file
with open(input_path, 'r') as file:
    data = json.load(file)

# Replace "auth_type": 1 with "type": "AUTHENTICATION_STORED_SPOTIFY_CREDENTIALS"
if "auth_type" in data and data["auth_type"] == 1:
    data["type"] = "AUTHENTICATION_STORED_SPOTIFY_CREDENTIALS"
    del data["auth_type"]

# Rename "auth_data" to "credentials"
if "auth_data" in data:
    data["credentials"] = data.pop("auth_data")

# Create the output directory if it doesn't exist
output_path.parent.mkdir(parents=True, exist_ok=True)

# Save the modified JSON data to the output file, replacing any existing file
with open(output_path, 'w') as file:
    json.dump(data, file, indent=4)

print(f'Modified credentials saved to {output_path}')
