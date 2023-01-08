import pandas as pd

from dictionary import Dictionary

dictionary = Dictionary()
dictionary_df = dictionary.dictionary_df

# Go through the "english_names" column and if the value in the cell is a list, place the list elements in
# separate columns. The number of additional columns is 5 (the maximum number of english names for a word).
# The new columns are named "english_name_0", "english_name_1", etc.

new_df = pd.DataFrame()

for index, row in dictionary_df.iterrows():
    english_names = row["english_names"]
    if isinstance(english_names, list):
        for i, english_name in enumerate(english_names):
            if i == 5:
                break
            row[f"english_name_{i}"] = english_name
    new_df = pd.concat([new_df, row.to_frame().T])

new_df = new_df.drop(columns=["english_names"])

new_df.to_csv("test_dictionary.csv", index=False)
print(new_df)
