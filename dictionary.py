from pathlib import Path
import requests
import re
from collections import namedtuple
import json
import bs4

from constants import *
from DataManagment.file_system import load_file, save_to_file


class Dictionary:
    DICTIONARY_URL = "https://api.pons.com/v1/dictionary"
    API_KEY_PATH = API_PATH / "key.txt"

    WORD_TYPES = namedtuple("word_type", ["NOUN", "VERB", "ADJECTIVE"])

    GENDERS = namedtuple("gender", ["MASCULINE", "FEMININE", "NEUTER"])("der", "die", "das")
    GENDER_ENCODING = {"nt": GENDERS.NEUTER, "m": GENDERS.MASCULINE, "f": GENDERS.FEMININE}

    NUM_MEANINGS_LIMIT = 5

    def __init__(self):
        key = load_file(self.API_KEY_PATH)["key"]
        self.header = {"X-Secret": key}

    def word_info(self, word: str) -> str:
        url = f"{self.DICTIONARY_URL}?l=deen&q={word}"
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            full_response = response.json()[0]["hits"][0]["roms"][0]
            headword_full = bs4.BeautifulSoup(full_response["headword_full"], "html.parser").get_text()
            headword_full_split = re.split(r"\[|<|>|]| |-|'|,", headword_full)
            word_data = [val for val in headword_full_split if val != ""]

            name = word_data[0]
            declension = word_data[1]
            plural = word_data[2]
            article = self.GENDER_ENCODING[word_data[-1]]

            meanings = []
            # -1 because the last element doesn't contain meaning information
            max_search_length = min(len(full_response["arabs"])-1, self.NUM_MEANINGS_LIMIT)
            for i in range(max_search_length):
                meaning_cleaned = bs4.BeautifulSoup(full_response["arabs"][i]["header"], "html.parser").get_text()
                meaning_cleaned = re.split("\(|\)", meaning_cleaned)[1]
                meanings.append(meaning_cleaned)
            save_to_file(full_response, API_PATH / "last_response.txt")

            headword_full = response.json()[0]["hits"][0]["roms"][0]["headword_full"]
            words_in_headword = re.split(r"[<>]", headword_full)
            article = self.GENDER_ENCODING[words_in_headword[-5]]
            return article
        else:
            return "No definition found."


some_dictionary = Dictionary()
print(some_dictionary.word_info("Haus"))


class Noun:
    def __init__(self, english_name: str, name: str = None, article: str = None, plural: str = None,
                 declension: str = None, meanings: list = None, dictionary: Dictionary = None):
        self.english_name = english_name
        if name is None or article is None or plural is None or declension is None or meanings is None:
            self.load_from_file()
