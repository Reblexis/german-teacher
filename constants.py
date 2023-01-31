from pathlib import Path
from collections import namedtuple

DATA_PATH = Path("Data")

# API
API_PATH = DATA_PATH / "API"

# Datasets
DATASETS_PATH = DATA_PATH / "Datasets"
RAW_DATASETS_PATH = DATASETS_PATH / "Raw"
CLEANED_DATASETS_PATH = DATASETS_PATH / "Cleaned"

# Dictionary
DICTIONARIES = DATASETS_PATH / "Dictionaries"
MAIN_DICTIONARY_PATH = DICTIONARIES / "Main"

GENDERS = namedtuple("gender", ["MASCULINE", "FEMININE", "NEUTER"])("der", "die", "das")
WORD_TYPES = namedtuple("word_type", ["NOUN", "VERB", "ADJECTIVE"])("noun", "verb", "adjective")

# Web
INTERFACE_PATH = Path("Interface")
WEB_MEDIA_PATH = INTERFACE_PATH / "Media"
ACCURACY_PLOT_PATH = WEB_MEDIA_PATH / "accuracy_plot.png"
