# German teacher

The goal of this app is to help you learn german rules and vocabulary. It is currently in development and therefore contains only core features.  
For the future, there is a plan to add an advanced statistics, more practice modes, a better feedback loop and background intelligence
that would allow for a more effective learning.

## Setup ##
So far only one setup has been tested:
- Windows 11
- Python 3.10.8 / 3.10.9

## Installation ##
1. Clone the repository
2. Install the requirements using `pip install -r requirements.txt`
3. Run the launcher.py file

## Word types ##
Each word is of a certain type.
The type of word is determined by the way
that the word is used in a sentence. 
The following types are supported so far (green): 
```diff
+ noun
- verb
- adjective
```
To each word type, there are certain characteristics which the word belonging to that type has.
For example car is a noun, and by nouns we characterize:
- english name: car
- name: Auto 
- article: das
- plural: Autos
- declension: des Autos
- meaning: ein Fahrzeug mit vier Rädern

By verbs, we characterize (for example - to be):
- english name: to be
- name: sein
- present tense: bin, bist, ist, sind, seid, sind
- past tense: war, warst, war, waren, wart, waren
- future tense: werde, wirst, wird, werden, werdet, werden
- past participle: gewesen
- auxiliary verb: sein
- meanings: [Eigenshaft haben; existieren; sich befinden; zutreffen; ...]

By adjectives, we characterize (for example - big):
- wort: groß
- comparative: größer
- superlative: am größten

## How to use ##
For each of these word types there is a lot of corresponding words saved in the database.
You can practice different rules by selecting them using the GUI.

## Screenshots ##
### Practice menu ###
![Screenshot](Documentation/Screenshots/practice_menu.png)
### Basic statistics ###
![Screenshot](Documentation/Screenshots/stats_menu.png)


