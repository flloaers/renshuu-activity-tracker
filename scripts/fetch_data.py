import sys 
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_fetcher import RenshuuDataFetcher

def main():
    """
    Fetch and log Renshuu data.
    """
    try:
        fetcher = RenshuuDataFetcher()
        success = fetcher.fetch_and_log()

        if success:
            print("✓ Successfully fetched and logged Renshuu data!")
        else:
            print("✗ Failed to fetch or log data.")

    except Exception as e: 
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 