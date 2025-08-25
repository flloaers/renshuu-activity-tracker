"""Script to generate all Renshuu visualisations."""

import sys 
import os 
import polars as pl 
import pandas as pd 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_processor import load_and_process_data
from src.visualizer import RenshuuVisualizer
from config.settings import LOG_FILE 


def _ensure_pandas(df) -> pd.DataFrame:
    """
    Convert Polars DataFrame to Pandas.
    """
    if isinstance(df, pl.DataFrame):
        return df.to_pandas()
    return df

def main():
    """
    Generate all plots from logged data.
    """
    print("Loading and processing Renshuu data...")

    try: 
        # Load data.
        df_daily, df_progress, snapshots = load_and_process_data(LOG_FILE)
        
        if df_daily.is_empty() and df_progress.is_empty():
            print("No data available. Run fetch_data.py first.")
            sys.exit(1)

        df_daily = _ensure_pandas(df_daily)
        df_daily = df_daily.set_index("fetch_date")

        df_progress = _ensure_pandas(df_progress)

        snapshots = {cat: _ensure_pandas(df) for cat, df in snapshots.items()}

        # Create visualizer.
        viz = RenshuuVisualizer()

        # Generate heatmaps. 
        if not df_daily.empty:
            print("Generating activity heatmaps...")
            viz.plot_all_activity_heatmaps(df_daily)
        else:
            print("No daily activity data available.")

        # Generate progress bars.
        if snapshots and not all(df.empty for df in snapshots.values()):
            print("Generating current progress bars...")
            viz.plot_current_progress_bars(snapshots)
        else:
            print("No progress snapshot available.")
             
        if not df_progress.empty:
            print("Generating progress time-evolution plots...")
            viz.plot_progress_over_time_multi_panel(df_progress)
        else:
            print("No progress data available.")

        print("✓ All visualisations generated successfully!")

    except Exception as e: 
        print(f"✗ Error generating plots: {e}.")
        sys.exit(1)

if __name__ == "__main__":
    main() 
