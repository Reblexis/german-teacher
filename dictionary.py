from pathlib import Path
import requests
import re
from collections import namedtuple
import json
import bs4
from typing import Union

from constants import *
from DataManagment.file_system import load_file, save_to_file


class Dictionary:
    DICTIONARY_URL = "https://api.pons.com/v1/dictionary"
    API_KEY_PATH = API_PATH / "key.txt"

    GENDER_ENCODING = {"nt": GENDERS.NEUTER, "m": GENDERS.MASCULINE, "f": GENDERS.FEMININE, None: None}
    WORD_TYPE_ENCODING = {"N": WORD_TYPES.NOUN, "VB": WORD_TYPES.VERB, "ADJ": WORD_TYPES.ADJECTIVE, None: None}

    NUM_MEANINGS_LIMIT = 5

    def __init__(self):
        key = load_file(self.API_KEY_PATH)["key"]
        self.header = {"X-Secret": key}
        self.searched_space = None

    def find(self, class_name: str):
        soup = bs4.BeautifulSoup(self.searched_space, "html.parser")
        data = soup.find(class_=class_name)
        if data is None:
            return None
        return data.get_text()

    def word_info(self, word: str) -> Union[dict, str]:
        info = {"name": word}
        url = f"{self.DICTIONARY_URL}?l=deen&q={word}"
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            full_response = response.json()[0]["hits"][0]["roms"][0]
            headword_full = full_response["headword_full"]

            self.searched_space = headword_full
            word_type = self.WORD_TYPE_ENCODING[self.find("wordclass")]

            assert word_type == WORD_TYPES.NOUN, f"Word type is not noun: {word_type}"
            info["word_type"] = word_type

            info["article"] = self.GENDER_ENCODING[self.find("genus")]
            info["flexion"] = self.find("flexion")
            if info["flexion"] is not None:
                info["flexion"] = info["flexion"].replace(" ", "").replace("<", "").replace(">", "")
                info["flexion"] = info["flexion"].split(",")

            info["meanings"] = []
            info["english_names"] = []

            # -1 because the last element doesn't contain meaning information
            max_search_length = min(len(full_response["arabs"]), self.NUM_MEANINGS_LIMIT)
            for i in range(max_search_length):
                arab = full_response["arabs"][i]
                meaning_cleaned = bs4.BeautifulSoup(arab["header"], "html.parser").get_text()
                if "(" not in meaning_cleaned and meaning_cleaned != "":
                    break
                meaning_cleaned = re.split("\(|\)", meaning_cleaned)[1] if "(" in meaning_cleaned else None
                info["meanings"].append(meaning_cleaned)
                english_name = bs4.BeautifulSoup(arab["translations"][0]["target"], "html.parser").get_text()
                info["english_names"].append(english_name)

            save_to_file(full_response, API_PATH / "last_response.txt")
            return info
        else:
            return "No definition found."


class Noun:
    def __init__(self, name: str, english_names: list = None, article: str = None, plural: str = None,
                 declension: str = None, meanings: list = None, dictionary: Dictionary = None):

        if english_names is None or article is None or plural is None or declension is None or meanings is None:
            assert dictionary is not None, "If you don't provide all the information, you must provide a dictionary."
            word_info = {"declension": None}
            received_info = dictionary.word_info(name)
            if isinstance(word_info, str):
                raise ValueError(word_info)
            word_info.update(received_info)

            english_names = word_info["english_names"]
            article = word_info["article"]
            flexion = word_info["flexion"]
            plural = flexion[1] if (flexion is not None and len(flexion) > 1) else None
            declension = word_info["flexion"][0] if flexion is not None else None
            meanings = word_info["meanings"]

        self.name = name
        self.english_names = english_names
        self.article = article
        self.plural = plural
        self.declension = declension
        self.meanings = meanings

    def __str__(self):
        return f"{self.article} {self.name} ({self.plural}) - {self.english_names}"

    def meanings(self):
        return self.meanings


if __name__ == "__main__":
    test_dictionary = Dictionary()
    noun = Noun("Silber", dictionary=test_dictionary)
    print(noun)
    print(noun.meanings)
