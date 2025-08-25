# 📈 Renshuu Activity Tracker 

A Python tool for tracking and visualising Renshuu learning progress using various visualisations.

## Why this Project? 
I wanted to track my Japanese learning consistency and see my progress over time in a visual way. Since Renshuu provides an API, I built this tool to automatically collect my daily study data and create visualisations.

## 📋 Requirements
- Renshuu account with API access
- Python 3.9+
- uv package manager (`pip install uv`)

##  🌟 Features 
- **Daily Activity Tracking**: Fetch your daily study metrics from Renshuu API. 
- **Calendar Heatmaps**: GitHub-style activity visualisation for different study categories. 
- **Current Progress Bars**: Snapshot of your progress across all JLPT levels.
- **Time Evolution of Progress**: Multi-panel line charts showing progression over time.

## 🐻‍❄️ Choice of DataFrames: Polars + Pandas
Since my data log is quite small and plotting packages typically feed on Pandas DataFrames, I could have chosen Pandas all over, but I love the syntax of Polars... so I use Polars for data processing and convert to Pandas only for plotting compatibility. 

## 📊 What You Will Get
After running the scripts, you will find plots like:
- `daily_activity_heatmap.png` - GitHub-style study streak visualization
- `current_progress.png` - JLPT level progress bars  
- `progress_over_time.png` - Historical learning trends

## 🚀 Quick Start
> Note: This project uses [uv](https://uv.run/) as a lightweight package manager and script runner.  
> Install it via `pip install uv` if not already available.

### Clone the Repository 
```console 
git clone https://github.com/yourusername/renshuu-activity-tracker.git
cd renshuu-activity-tracker
```
### Install Dependencies 
```
uv sync 
```
> This automatically creates a virtual environment (`.venv/`) and installs all dependencies. 
### Configure Environment Variables 
Create a `.env` file in the `config/` folder.
```console 
REN_API_KEY=your_personal_api_key
API_BASE_URL=https://api.renshuu.org/v1
LOG_FILE_PATH=data/renshuu_logs.jsonl
PLOTS_DIR=plots 
```
When logged in the [Renshuu website](https://www.renshuu.org), you can find your API key via the [**Resources** menu](https://www.renshuu.org/index.php?page=misc/api).

### Collect Your First Data 
```
uv run python scripts/fetch_data.py
```
> This fetches your study logs and stores them in the `data/` folder.

### Generate Visualisations 
```
uv run python scripts/generate_plots.py
```
> This generates calendar heatmaps, current progress bars, and multi-panel progress charts in the `plots/` folder. 



## 📁 Project Structure 

```
├── config/                     # Settings, configurations, and .env file
├── src/                        # Core modules
|    ├── data_fetcher.py            # API calls and logging
|    ├── data_processor.py          # Data processing with Polars
|    └── visualizer.py              # Plot generation
├── scripts/                    # Main entry points 
|    ├── fetch_data.py              # Data collection
|    └── generate_plots.py          # Visualisation generation
├── data/                       # Study logs
├── plots/                      # Generated visualisations
├── pyproject.toml              # Project configuration and dependencies
├── uv.lock                     # Locked dependency versions (auto-generated)
├── requirements.txt            # Alternative pip-compatible dependencies
└── README.md
```

## 📄 License
MIT License - feel free to use and modify!

## 🤝 Contributing
Issues and pull requests welcome! This is a learning project, so feedback is appreciated.

## 🔌 API Usage Notes
⚠️ **Rate Limiting**: Be mindful of Renshuu's API limits. The current setup is meant to fetch data once daily, which is well within reasonable limits. 

## 🔧 Troubleshooting
- **API Key Issues**: Ensure your key is correctly set in the `.env` file.
- **Missing Directories**: The script will create `data/` and `plots/`. folders automatically.
- **Import Errors**: Run `uv sync` to ensure all dependencies are installed.

## ⏰ Automation Setup 
**Linux/macOS** (crontab):
Create a wrapper script for reliable cron execution.

**Create `scripts/run_daily.sh`:**
```console
#!/bin/bash
export PATH="$PATH:/home/username/.local/bin"
cd /full/path/to/your/renshuu-activity-tracker
uv run python scripts/fetch_data.py 
```
**Make executable and add to crontab:**
``` console 
chmod +x scripts/run_daily.sh
crontab -e
# Add: 0 20 * * * /full/path/to/your/renshuu-activity-tracker/scripts/run_daily.sh
```

**Windows** (Task Scheduler): Set up a daily task to run the ``fetch_data.py`` script. 