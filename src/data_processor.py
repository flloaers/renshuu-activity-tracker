import os
import polars as pl 
import pandas as pd 
from typing import Tuple, Dict
from config.settings import CATEGORIES, LEVELS 

class RenshuuDataProcessor: 
    """
    Processes Renshuu log data for visualisation.
    Fully Polars-flavoured.
    """

    @staticmethod 
    def load_and_deduplicate_logs(log_file_path: str) -> pl.DataFrame:
        """
        Load and deduplicate Renshuu log data.
        """
        if not os.path.exists(log_file_path):
            print(f"Error: Log file '{log_file_path}' not found.")
            return pl.DataFrame()
    
        try:
            df = pl.read_ndjson(log_file_path)

            # Convert 'fetch_timestamp' string to a Polars Datetime column. 
            df = df.with_columns([
                pl.col("fetch_timestamp")
                .str.strptime(pl.Datetime, format="%Y-%m-%dT%H:%M:%S%.f")
                .alias("full_timestamp"),
            ])

            # Extract the date part from the 'full_timestamp' Datetime column.
            df = df.with_columns([
                pl.col("full_timestamp").dt.date().alias("fetch_date")
            ])

            # Sort and deduplicate.
            df = df.sort("full_timestamp")
            deduplicated_df = df.unique(subset=["fetch_date"], keep="last")

            print(f"Successfully loaded {len(deduplicated_df)} daily entries.")
            return deduplicated_df 

        except Exception as e:
            print(f"Error loading data: {e}.")
            return pl.DataFrame()
        
    @staticmethod
    def extract_daily_activity_metrics(deduplicated_df: pl.DataFrame) -> pl.DataFrame:
        """
        Extract daily activity metrics.
        """
        if deduplicated_df.is_empty():
            return pl.DataFrame()
        
        df_daily_metrics = deduplicated_df.select([
            pl.col("fetch_date").cast(pl.Datetime), 
            pl.col("studied").struct.field("today_all").fill_null(0).alias("daily_all"),
            pl.col("studied").struct.field("today_grammar").fill_null(0).alias("daily_grammar"),
            pl.col("studied").struct.field("today_vocab").fill_null(0).alias("daily_vocab"),
            pl.col("studied").struct.field("today_kanji").fill_null(0).alias("daily_kanji"),
            pl.col("studied").struct.field("today_sent").fill_null(0).alias("daily_sent"),
        ]).sort("fetch_date")

        return df_daily_metrics 
    
    @staticmethod 
    def extract_level_progress_metrics(deduplicated_df: pl.DataFrame) -> pl.DataFrame:
        """
        Extract level progress metrics in long format.
        """
        if deduplicated_df.is_empty():
            return pl.DataFrame()
                
        # Unnest level_progress_percs.
        df_progress = deduplicated_df.select([
            pl.col("fetch_date"),
            pl.col("level_progress_percs")
        ]).unnest("level_progress_percs")

        # Create expressions for each category-level combination.
        expressions = [pl.col("fetch_date")]
        for category in CATEGORIES.keys():
            for level in LEVELS:
                expressions.append(
                    pl.col(category).struct.field(level)
                        .fill_null(0)
                        .alias(f"{category}_{level}")
                )
        
        df_flat = df_progress.select(expressions).sort("fetch_date")
        id_vars = ["fetch_date"]
        value_vars = [col for col in df_flat.columns if col not in id_vars]

        df_long = df_flat.unpivot(
            on=value_vars,
            index=id_vars,
            variable_name="metric_level",
            value_name="percentage"
        ).with_columns([
            pl.col("metric_level").str.split_exact("_", 1).struct.field("field_0").alias("category"),
            pl.col("metric_level").str.split_exact("_", 1).struct.field("field_1").alias("level")
        ])
        
        return df_long 

    @staticmethod
    def get_latest_progress_snapshot(deduplicated_df: pl.DataFrame) -> Dict[str, pl.DataFrame]:
        """
        Get the latest snapshot of progress per category for bar charts or heatmap matrices.
        Returns a dictionary {category: DataFrame} 
        """        
        if deduplicated_df.is_empty():
            return {}
    
        latest_date = deduplicated_df.select(
            pl.col("fetch_date").max()
        ).item()
        latest_data = deduplicated_df.filter(
            pl.col("fetch_date") == latest_date
        )

        snapshots = {}
        for cat in CATEGORIES.keys():
            df_cat = latest_data.select([
                pl.col("level_progress_percs").struct.field(cat)
            ]).unnest(cat).sort(by=LEVELS)

            snapshots[cat] = df_cat 

        return snapshots



def load_and_process_data(log_file_path: str) -> Tuple[pl.DataFrame, pl.DataFrame, Dict[str, pl.Series]]:
    """
    Load and process raw data into daily metrics, long-format progress metrics,
    and the latest snapshot of progress by category.
    Returns (daily_metrics, progress_metrics, snapshots).
    """
    processor = RenshuuDataProcessor()
    # Load and deduplicate.
    deduplicated_df = processor.load_and_deduplicate_logs(log_file_path)

    if deduplicated_df.is_empty():
        return pl.DataFrame(), pl.DataFrame(), 
    
    # Extract metrics.
    daily_metrics = processor.extract_daily_activity_metrics(deduplicated_df)
    progress_metrics = processor.extract_level_progress_metrics(deduplicated_df)
    snapshots = processor.get_latest_progress_snapshot(deduplicated_df)

    return daily_metrics, progress_metrics, snapshots