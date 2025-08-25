import os 
import sys 
import requests 
import json 
from datetime import datetime 
from typing import Dict, Any, Optional 
from config.settings import REN_API_KEY, API_BASE_URL, LOG_FILE

class RenshuuDataFetcher: 
    """
    Handles fetching data from Renshuu API and logging to JSONL files.
    """

    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or REN_API_KEY
        self.base_url = base_url or API_BASE_URL
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

        if not self.api_key: 
            raise ValueError("API key not found. Please set REN_API_KEY in your .env file.")
        
    def fetch_profile(self) -> Optional[Dict[str, Any]]:
        """
        Fetch profile data from Renshuu API.
        """
        profile_url = f"{self.base_url}/profile"

        try:
            response = requests.get(profile_url, headers=self.headers)
            response.raise_for_status() 
            return response.json()
    
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}.")
            print(f"Response content: {response.text}")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}.")
        except requests.exceptions.Timeout as e:
            print(f"Timeout error: {e}.")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}.")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}.")
            print(f"Raw response: {response.text}")

        return None 
    
    def save_to_log(self, data: Dict[str, Any], log_file: str = None) -> bool: 
        """
        Save data to JSONL log file. 
        """
        log_file = log_file or LOG_FILE 

        data['fetch_timestamp'] = datetime.now().isoformat()

        try: 
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            with open(log_file, 'a', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
                f.write('\n')
            return True 
    
        except IOError as e:
            print(f"Error writing to log file {log_file}: {e}.")
            return False 
        
    def fetch_and_log(self, log_file: str = None) -> bool: 
        """
        Fetch profile data and log it. 
        Returns True if successful. 
        """
        data = self.fetch_profile()
        if data:
            return self.save_to_log(data, log_file)
        return False 