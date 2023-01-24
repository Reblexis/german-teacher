# Developer documentation #

## Introduction ##
This document is intended to help developers to understand the code of the project.
Please read the main readme and the user documentation first. 

## Code structure ##
The code is composed of the web app (composed of HTML, CSS and JS) and the python that controls
the dynamic behaviour of the app. The naming of files / folders follows the following convention:
- `snake_case` for files
- `CamelCase` for folders

## Data ##
The project contains also a data folder which can be placed anywhere in the computer (currently placed in the project, however normally it would be installed separately).
It's composed of bigger files and saves.
The data folder contains the following files:
- API files (Data/API): these files are necessary for communication with one of the two APIs used in the project (PONS).
- Datasets (Data/Datasets): word lists that were used to generate dictionary for the project (Raw folder) as well as the dictionary (Cleaned folder).
- Statistics: doesn't contain anything by default but is used to save statistics of the user.

### Dictionary ###
The dictionary is saved into .pickle format because .pickle saves the variable types (e.g. list, dict, etc.) and is therefore more convenient to use.
The original type is a pandas DataFrame and contains the following columns:
- 'name': the German word
- 'article': the article of the word (der, die, das)
- 'flexion': plural, past tense, etc.
- 'meaning': meaning in German
- 'english_names': possible English translations  

Dictionary contains unique entries (no duplicates).

### Statistics ###
Currently, there is only one statistic tracked: guesses and their correctness. This is saved into 'guesses.pickle' file (there is also guesses.csv (which contains the same content) file saved simultaneously for debugging purposes).
The original type of the 'guesses.pickle' file is a pandas DataFrame and contains the following columns: 
- 'category': the category of the task, where the answer was recorded (e.g. articles, translation, meaning)
- 'name': the German word
- 'guess': the answer given by the user
- 'correct_answer': the correct answer
- 'is_correct': whether the guess matches the correct answer
- 'time': date and time of the guess

## Web app ##
The web app can be found in the 'Interface' folder and is composed of the following files:
- main_menu.html : the only html file of the app it contains all static elements of the app
- style.css : contains all styling of the html elements
- ui.js: contains all dynamic behaviour of the app UI
- practice.js: communicates with python regarding practice and manages practice panel. Contains basic logic for practice modes.
- statistics.js: communicates with python regarding statistics and manages statistics panel. Contains basic logic for statistics modes.
Every media regarding the app should be placed in the Interface/Media folder.

## Python ##
The python code can be split in the following way:
- basic management scripts
- dictionary related scripts
- practice and statistics modules

### Basic management scripts ###
- launcher.py: launches the app
- constants.py: contains all shared constants used in the app
- DataManagement/file_system.py: contains all functions related to file system management

### Dictionary related scripts ###
- Dictionary/dictionary.py: contains the dictionary class which is responsible for all communication with APIs. It also contains the Noun class (represents nouns and their individual properties) and the DictionaryController class (allows for effective retrieval of words from dictionary).

### Practice and statistics modules ###
- Practice/practice.py: contains a practice controller class which is responsible for all core mechanics regarding the practice modes. It generates questions, checks answers, calls statistics update, etc. .
- Statistics/statistics.py: contains a statistics controller class that is responsible for collecting statistics and saving them appropriately. Currently, it also supports plotting of a graph of accuracy over time.