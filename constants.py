from pathlib import Path
from collections import namedtuple

DATA_PATH = Path("C:/Data/GermanTeacher")

# API
API_PATH = DATA_PATH / "API"

# Dictionary
GENDERS = namedtuple("gender", ["MASCULINE", "FEMININE", "NEUTER"])("der", "die", "das")
WORD_TYPES = namedtuple("word_type", ["NOUN", "VERB", "ADJECTIVE"])("noun", "verb", "adjective")