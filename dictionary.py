from pathlib import Path
import requests
import re
from collections import namedtuple

from DataManagment.file_system import load_file


class Dictionary:
    DICTIONARY_URL = "https://api.pons.com/v1/dictionary"
    SECRET_KEY_PATH = Path("secret.txt")
    GENDERS = namedtuple("gender", ["MASCULINE", "FEMININE", "NEUTER", "PLURAL"])("masculine", "feminine", "neuter",
                                                                                  "plural")
    GENDER_ENCODING = {"nt": GENDERS.NEUTER, "m": GENDERS.MASCULINE, "f": GENDERS.FEMININE, "pl": GENDERS.PLURAL}

    def __init__(self):
        key = load_file(self.SECRET_KEY_PATH)["key"]
        self.header = {"X-Secret": key}

    def word_definition(self, word: str) -> str:
        url = f"{self.DICTIONARY_URL}?l=deen&q={word}"
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            headword_full = response.json()[0]["hits"][0]["roms"][0]["headword_full"]
            words_in_headword = re.split(r"[<>]", headword_full)
            gender = self.GENDER_ENCODING[words_in_headword[-5]]
            return gender
        else:
            return "No definition found."


dictionary = Dictionary()
print(dictionary.word_definition("Haus"))

