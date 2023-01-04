import pandas as pd
from pathlib import Path
import re

from DataManagment.file_system import load_file
from dictionary import Dictionary, Noun

NOUNS_PATH = Path("nouns.txt")
nouns = load_file(NOUNS_PATH, additional_info={"type": "lines"})
german_names = []
dictionary = Dictionary()

for noun in nouns:
    vals = re.split(r"[–~\n.]", noun)
    vals = [val for val in vals if val != ""]
    vals = [val.strip() for val in vals]
    english_name, german_name, plural = vals[1:]
    german_name = german_name.split(" ")[-1]
    try:
        noun = Noun(german_name, dictionary=dictionary)
        print(noun)
    except KeyError:
        print(f"KeyError: {german_name}")
        continue
    except TypeError:
        print(f"TypeError: {german_name}")
        continue
    except ValueError:
        print(f"ValueError: {german_name}")
        continue


df = pd.DataFrame({"english_name": english_names, "german_name": german_names, "plural": plurals})
df.to_csv("nouns.csv", index=False)
