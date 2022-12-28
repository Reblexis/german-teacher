import pandas as pd
from pathlib import Path
import re

from DataManagment.file_system import load_file

NOUNS_PATH = Path("nouns.txt")
nouns = load_file(NOUNS_PATH, additional_info={"type": "lines"})
print(nouns[0])
english_names = []
genders = []
german_names = []
plurals = []

for noun in nouns:
    vals = re.split(r"[–~\n.]", noun)
    vals = [val for val in vals if val != ""]
    vals = [val.strip() for val in vals]
    english_name, german_name, plural = vals[1:]
    english_names.append(english_name)
    german_names.append(german_name)
    plurals.append(plural)

df = pd.DataFrame({"english_name": english_names, "german_name": german_names, "plural": plurals})
df.to_csv("nouns.csv", index=False)
