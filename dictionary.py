import requests
import re
import bs4
from typing import Union
import pandas as pd
import ast

from constants import *
from DataManagment.file_system import load_file, save_to_file


class Dictionary:
    DICTIONARY_PATH = CLEANED_DATASETS_PATH / "dictionary.pickle"
    DICTIONARY_URL = "https://api.pons.com/v1/dictionary"
    API_KEY_PATH = API_PATH / "key.txt"

    GENDER_ENCODING = {"nt": GENDERS.NEUTER, "m": GENDERS.MASCULINE, "f": GENDERS.FEMININE, None: None}
    WORD_TYPE_ENCODING = {"N": WORD_TYPES.NOUN, "VB": WORD_TYPES.VERB, "ADJ": WORD_TYPES.ADJECTIVE, None: None}

    NUM_MEANINGS_LIMIT = 5

    RESET = False

    def __init__(self):
        key = load_file(self.API_KEY_PATH)["key"]
        self.header = {"X-Secret": key}
        self.searched_space = None

        if not self.DICTIONARY_PATH.exists() or self.RESET:
            # Create dictionary with a useless row to prevent bugs
            example = {"name": "test_name", "article": "test_article", "flexion": "test_flexion",
                       "meanings": "test_meanings", "word_type": "test_type", "english_names": "test_english_names"}
            self.dictionary = pd.DataFrame()
            self.save_to_local_dictionary(example)

        self.dictionary = pd.read_pickle(self.DICTIONARY_PATH) if self.DICTIONARY_PATH.exists() else pd.DataFrame()

    def find(self, class_name: str):
        soup = bs4.BeautifulSoup(self.searched_space, "html.parser")
        data = soup.find(class_=class_name)
        if data is None:
            return None
        return data.get_text()

    def save_to_local_dictionary(self, info: dict):
        self.dictionary = pd.concat([self.dictionary, pd.DataFrame([info])])
        self.dictionary.to_pickle(self.DICTIONARY_PATH)

    def word_info(self, german_name: str) -> Union[dict, str]:
        if len(self.dictionary[self.dictionary["name"] == german_name]) > 0:
            print("Loaded from local dictionary!")
            return self.dictionary[self.dictionary["name"] == german_name].iloc[0].to_dict()

        info = {"name": german_name, "article": None, "flexion": None, "meanings": None, "english_names": None}
        url = f"{self.DICTIONARY_URL}?l=deen&q={german_name}"
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            full_response = response.json()[0]["hits"][0]["roms"][0]
            headword_full = full_response["headword_full"]

            self.searched_space = headword_full

            info["word_type"] = self.WORD_TYPE_ENCODING[self.find("wordclass")]
            if info["word_type"] != WORD_TYPES.NOUN:
                return info

            info["article"] = self.GENDER_ENCODING[self.find("genus")]
            info["flexion"] = self.find("flexion")
            if info["flexion"] is not None:
                info["flexion"] = info["flexion"].replace(" ", "").replace("<", "").replace(">", "")
                info["flexion"] = info["flexion"].split(",")

            info["meanings"] = []
            info["english_names"] = []

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
            print(response.status_code)
            return "No definition found."


class Noun:
    def __init__(self, name: str, english_names: list = None, article: str = None, plural: str = None,
                 declension: str = None, meanings: list = None, dictionary: Dictionary = None):

        if english_names is None or article is None or plural is None or declension is None or meanings is None:
            assert dictionary is not None, "If you don't provide all the information, you must provide a dictionary."
            word_info = {"declension": None}
            received_info = dictionary.word_info(name)
            word_info.update(received_info)

            if word_info["word_type"] != WORD_TYPES.NOUN:
                raise TypeError(f"'{name}' is not a noun.")

            english_names = word_info["english_names"]
            article = word_info["article"]
            flexion = word_info["flexion"]
            plural = flexion[1] if (flexion is not None and len(flexion) > 1) else None
            declension = word_info["flexion"][0] if flexion is not None else None
            meanings = word_info["meanings"]
            dictionary.save_to_local_dictionary(word_info)

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
    noun = Noun("Hand", dictionary=test_dictionary)
    print(noun)
    print(noun.meanings)
