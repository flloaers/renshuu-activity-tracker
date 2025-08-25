import os 
from dotenv import load_dotenv 

load_dotenv(dotenv_path="config/.env")

# API Configuration 
REN_API_KEY = os.getenv("REN_API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL")

# File paths 
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
PLOTS_DIR = os.path.join(PROJECT_ROOT, "plots")
LOG_FILE = os.path.join(DATA_DIR, "renshuu_logs.jsonl")

# Study categories and levels 
CATEGORIES = {
    'vocab': 'Vocabulary', 
    'grammar': 'Grammar', 
    'kanji': 'Kanji', 
    'sent': 'Sentences'
}

LEVELS = ['n5', 'n4', 'n3', 'n2', 'n1']

METRICS = {
    'daily_all': 'Overall Activity',
    'daily_vocab': 'Vocabulary',
    'daily_grammar': 'Grammar',
    'daily_kanji': 'Kanji',
    'daily_sent': 'Sentences'
}

# Plot settings 
PLOT_STYLE = {
    'cmap': 'YlGn', 
    'dpi': 300, 
    'figsize': (12, 8)
}

