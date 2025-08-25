import os 
import numpy as np 
import pandas as pd 
import polars as pl
import matplotlib.pyplot as plt 
import calplot 
from typing import Optional, List 
from config.settings import CATEGORIES, LEVELS, METRICS, PLOTS_DIR, PLOT_STYLE 

class RenshuuVisualizer: 
    """
    Handles visualisation of Renshuu study data.
    """

    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or PLOTS_DIR 
        os.makedirs(self.output_dir, exist_ok=True)


    def plot_activity_heatmap(self, data_series: pd.Series, title: str, 
                              metric_filename: str, save: bool = True) -> None:
        """
        Generate calendar heatmap for study activity.
        """
        if data_series.empty: 
            print(f"Cannot plot '{title}': Data series is empty.")
            return 
                        
        fig, ax = calplot.calplot(
            data_series, 
            cmap=PLOT_STYLE['cmap'],
            colorbar=False, 
            yearlabel_kws={'fontname': 'sans-serif'},
            suptitle=f"Renshuu Daily {title} Heatmap"
        )

        plt.tight_layout()

        if save:
            filename = os.path.join(
                self.output_dir, 
                f"renshuu_daily_{metric_filename}_heatmap.png"
            )
            fig.savefig(filename, dpi=PLOT_STYLE['dpi'], bbox_inches="tight")
            print(f"Heatmpap saved to {filename}.")

            plt.show()
            plt.close(fig) 

    def plot_all_activity_heatmaps(self, df_daily_metrics: pd.DataFrame) -> None: 
        """
        Generate heatmaps for all activity metrics.
        """
        if df_daily_metrics.empty: 
            print(f"No daily metrics data available for plotting.")
            return 
        
        for metric_col, title in METRICS.items():
            if metric_col in df_daily_metrics.columns: 
                self.plot_activity_heatmap(
                    df_daily_metrics[metric_col],
                    title, 
                    metric_col.replace('daily_', '')
                )

    def plot_progress_over_time_multi_panel(self, df_progress_long: pd.DataFrame, 
                                  levels_to_plot: List[str] = None, 
                                  save: bool = True
                                  ) -> None:
        """
        Generate multi-panel line charts showing the time evolution of progress 
        for each category and level.
        """
        levels_to_plot = levels_to_plot or LEVELS 

        if df_progress_long.empty: 
            print("No progress data available.")
            return 
        
        # Create subplots, one per category 
        n_categories = len(CATEGORIES)
        fix, axes = plt.subplots(2, 2, figsize=(15, 10))
        axes = axes.flatten() 

        for i, (category, category_label) in enumerate(CATEGORIES.items()):
            category_data = df_progress_long[df_progress_long['category'] == category]

            if category_data.empty:
                axes[i].text(0.5, 0.5, f"No {category_label} data",
                             ha='center', va='center', transform=axes[i].transAxes)
                continue

            # Plot each level as a separate line 
            for level in levels_to_plot:
                level_data = category_data[category_data['level'] == level]
                if not level_data.empty:
                    axes[i].plot(level_data['fetch_date'], level_data['percentage'],
                                 marker='o', label=level.upper(), linewidth=2, markersize=4)
                    
            axes[i].set_title(f"{category_label} Progress", fontweight='bold')
            axes[i].set_ylabel("Progress %")
            axes[i].legend(loc='best')
            axes[i].grid(True, alpha=0.3)
            axes[i].set_ylim(0, 100)

            # Rotate x-axis labels for better readability 
            axes[i].tick_params(axis='x', rotation=45)

        plt.suptitle("Learning Progress Over Time Across All Categories", fontsize=16, y=0.98)
        plt.tight_layout()

        if save: 
            filename = os.path.join(self.output_dir, "renshuu_progress_over_time.png")
            plt.savefig(filename, bbox_inches='tight', dpi=PLOT_STYLE['dpi'])
            print(f"Multi-panel chart saved to {filename}.")
        
        plt.show()
        plt.close()

    def plot_current_progress_bars(self, snapshots: dict, 
                                   levels_to_plot: List[str] = None,
                                   save: bool = True
                                   ) -> None:
        """
        Generate horizontal bar chart for latest progress snapshot using precomputed snapshots.
        """
        levels_to_plot = levels_to_plot or LEVELS 

        if not snapshots or all(df.empty for df in snapshots.values()):
            print("No progress snapshot available.")
            return 
        
        fig, ax = plt.subplots(figsize=(12, 8))

        y_pos = np.arange(len(levels_to_plot))
        bar_width = 0.2
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

        for i, (category, category_label) in enumerate(CATEGORIES.items()):
            df_cat = snapshots[category]
            values = [df_cat[level].iloc[0] if level in df_cat.columns else 0 for level in levels_to_plot] 

            ax.barh(y_pos + i * bar_width, values, bar_width, 
                    label=category_label, color=colors[i % len(colors)], alpha=0.8)
            
            # Add labels on bars 
            for j, value in enumerate(values):
                if value > 5:
                    ax.text(value / 2, y_pos[j] + i * bar_width, f"{value:.0f}%",
                            ha='center', va='center', fontweight='bold', color='white')
            
        ax.set_xlabel("Progress Percentage")
        ax.set_ylabel("JLPT Level")
        ax.set_title("Current Progress Snapshot", fontsize=14, pad=20)
        ax.set_yticks(y_pos + bar_width * 1.5)
        ax.set_yticklabels([lvl.upper() for lvl in levels_to_plot])
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_xlim(0, 100)
        ax.grid(axis='x', alpha=0.3)

        plt.tight_layout()

        if save: 
            filename = os.path.join(self.output_dir, "renshuu_progress_bars.png")
            plt.savefig(filename, bbox_inches='tight', dpi=PLOT_STYLE['dpi'])
            print(f"Current progress chart saved to {filename}.")

        plt.show()
        plt.close()
