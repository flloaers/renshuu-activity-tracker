import os
import sys
import requests
import json
import polars as pl

from dotenv import load_dotenv
from datetime import datetime

# --- Load environment variables from .env file ---
load_dotenv()

# --- Configuration ---
REN_API_KEY = os.getenv("REN_API_KEY") # Get API key from environment variable
API_BASE_URL = "https://api.renshuu.org/v1"
LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "renshuu_logs.jsonl")

if not REN_API_KEY:
    print("Error: REN_API_KEY not found in .env file or environment variables.")
    print("Please create a .env file with REN_API_KEY=\"YOUR_ACTUAL_API_KEY_HERE\"")
    sys.exit(1)

# --- Fetch Data from Renshuu API ---
profile_url = f"{API_BASE_URL}/profile"
headers = {
    "Authorization": f"Bearer {REN_API_KEY}"
}

try:
    response = requests.get(profile_url, headers=headers)
    response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
    profile_data = response.json()
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print(f"Response content: {response.text}")
    sys.exit(1)
except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err}")
    print("Please check your internet connection or the API URL.")
    sys.exit(1)
except requests.exceptions.Timeout as timeout_err:
    print(f"Timeout error occurred: {timeout_err}")
    print("The request took too long. Try again later.")
    sys.exit(1)
except requests.exceptions.RequestException as req_err:
    print(f"An unexpected error occurred: {req_err}")
    sys.exit(1)
except json.JSONDecodeError as json_err:
    print(f"Error decoding JSON response: {json_err}")
    print(f"Raw response: {response.text}")
    sys.exit(1)

# --- Add Timestamp to the Data ---
profile_data['fetch_timestamp'] = datetime.now().isoformat()

# --- Save Data to Log File (JSON Lines) ---
try:
    # Ensure the 'data' directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f: # Open in append mode ('a')
        json.dump(profile_data, f, ensure_ascii=False) # Write the JSON object
        f.write('\n') # Add a newline to make it a valid JSON Line
    print(f"Successfully logged data to {LOG_FILE}") 
except IOError as io_err:
    print(f"Error writing to log file {LOG_FILE}: {io_err}")
    import sys
    sys.exit(1)
