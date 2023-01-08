import requests
import re
import bs4
from typing import Union
import pandas as pd
import ast
import googletrans
import numpy as np
import random

from constants import *
from DataManagement.file_system import load_file, save_to_file


class Dictionary:
    """
    Allows for API interaction and word info lookup. Also saves data to local dictionary
    for faster retrieval and less API communication. Uses two APIs: PONS and Google Translate.
    """
    DICTIONARY_PATH = CLEANED_DATASETS_PATH / "dictionary.pickle"
    DICTIONARY_URL = "https://api.pons.com/v1/dictionary"
    API_KEY_PATH = API_PATH / "key.txt"

    GENDER_ENCODING = {"nt": GENDERS.NEUTER, "m": GENDERS.MASCULINE, "f": GENDERS.FEMININE, None: None}
    WORD_TYPE_ENCODING = {"N": WORD_TYPES.NOUN, "VB": WORD_TYPES.VERB, "ADJ": WORD_TYPES.ADJECTIVE, None: None}
    GOOGLE_WORD_TYPE_ENCODING = {"noun": WORD_TYPES.NOUN, "verb": WORD_TYPES.VERB, "adjective": WORD_TYPES.ADJECTIVE,
                                 None: None}

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
            self.dictionary_df = pd.DataFrame()
            self.save_to_local_dictionary(example)

        self.google_translator = googletrans.Translator()

        # Load dictionary without the useless row
        self.dictionary_df = pd.read_pickle(self.DICTIONARY_PATH)
        self.dictionary_df = self.dictionary_df[self.dictionary_df["name"] != "test_name"]
        self.dictionary_df.drop_duplicates(subset="name", inplace=True)
        print(self.dictionary_df)

    def find(self, class_name: str):
        soup = bs4.BeautifulSoup(self.searched_space, "html.parser")
        data = soup.find(class_=class_name)
        if data is None:
            return None
        return data.get_text()

    def replace_local_dictionary(self, new_dictionary):
        # save current dictionary to a backup
        self.dictionary_df.to_pickle(self.DICTIONARY_PATH.parent / f"dictionary_backup_{random.randint(0,1000000000)}.pickle")
        self.dictionary_df = new_dictionary
        self.dictionary_df.to_pickle(self.DICTIONARY_PATH)

    def save_to_local_dictionary(self, info: dict):
        if len(self.dictionary_df[self.dictionary_df["name"] == info["name"]]) > 0:
            return
        self.dictionary_df = pd.concat([self.dictionary_df, pd.DataFrame([info])])
        self.dictionary_df.to_pickle(self.DICTIONARY_PATH)

    def word_info(self, german_name: str) -> Union[dict, str]:
        if len(self.dictionary_df[self.dictionary_df["name"] == german_name]) > 0:
            print("Loaded from local dictionary!")
            return self.dictionary_df[self.dictionary_df["name"] == german_name].iloc[0].to_dict()

        german_name = german_name.capitalize()  # Ensuring that the word would be understood as noun

        info = {"name": german_name, "article": None, "flexion": None, "meaning": None, "english_names": None}
        url = f"{self.DICTIONARY_URL}?l=deen&q={german_name}"

        translation = self.google_translator.translate(german_name, src='de', dest="en")
        google_word_data = translation.extra_data
        google_word_type = self.GOOGLE_WORD_TYPE_ENCODING[google_word_data['all-translations'][0][0]]
        if google_word_type != WORD_TYPES.NOUN:
            print("Word is not a noun!")
            return "Word is not a noun!"

        response = requests.get(url, headers=self.header)

        if response.status_code == 200:
            full_response = response.json()[0]["hits"][0]["roms"][0]
            headword_full = full_response["headword_full"]

            self.searched_space = headword_full

            info["word_type"] = self.WORD_TYPE_ENCODING[self.find("wordclass")]
            if info["word_type"] != WORD_TYPES.NOUN:  # temporary, due to a lacking implementation of other types
                return info

            info["article"] = self.GENDER_ENCODING[self.find("genus")]
            info["flexion"] = self.find("flexion")
            if info["flexion"] is not None:
                info["flexion"] = info["flexion"].replace(" ", "").replace("<", "").replace(">", "")
                info["flexion"] = info["flexion"].split(",")

            info["meaning"] = google_word_data['definitions'][0][1][0][0]
            info["english_names"] = google_word_data['all-translations'][0][1]

            save_to_file(full_response, API_PATH / "last_response.txt")

            return info
        else:
            print(response.status_code)
            return "No definition found."


class Noun:
    def __init__(self, name: str, english_names: list = None, article: str = None, plural: str = None,
                 declension: str = None, meaning: str = None, dictionary: Dictionary = None):

        if english_names is None or article is None or plural is None or declension is None or meaning is None:
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
            meaning = word_info["meaning"]
            dictionary.save_to_local_dictionary(word_info)

        self.name = name
        self.english_names = english_names
        self.article = article
        self.plural = plural
        self.declension = declension
        self.meaning = meaning

    def __str__(self):
        return f"{self.article} {self.name} ({self.plural}) - {self.english_names}"

    def to_dict(self):
        return {"name": self.name, "english_names": self.english_names, "article": self.article, "plural": self.plural,
                "declension": self.declension, "meaning": self.meaning}

    def meaning(self):
        return self.meaning


class DictionaryController:
    def __init__(self):
        self.dictionary = Dictionary()
        self.dictionary_df = self.dictionary.dictionary_df

    def get_random_nouns(self, prioritized_property: str, count: int) -> list[Noun]:
        non_empty_property_rows = self.dictionary_df[self.dictionary_df[prioritized_property].notnull()]
        random_rows = non_empty_property_rows.sample(count, replace=False)

        return [Noun(row["name"], dictionary=self.dictionary) for _, row in random_rows.iterrows()]


if __name__ == "__main__":
    test_dictionary = Dictionary()
    print("Dictionary test:")
    noun = Noun("Hand", dictionary=test_dictionary)
    print(noun)
    print(noun.meaning)

    print("\nDictionary controller test:")
    dictionary_controller = DictionaryController()
    random_nouns = dictionary_controller.get_random_nouns("article", 4)
    print(random_nouns[0])
