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

### Web app ###
The web app can be found in the 'Interface' folder and is composed of the following files:
- main_menu.html : the only html file of the app it contains all static elements of the app
- style.css : contains all styling of the html elements
- ui.js: contains all dynamic behaviour of the app UI
- practice.js: communicates with python regarding practice and manages practice panel. Contains basic logic for practice modes.
- statistics.js: communicates with python regarding statistics and manages statistics panel. Contains basic logic for statistics modes.

### Python ###
The python code can be split in the following way:
- basic management scripts
- dictionary related scripts
- practice and statistics modules

#### Basic management scripts ####
- launcher.py: launches the app
- constants.py: contains all shared constants used in the app
- DataManagement/file_system.py: contains all functions related to file system management

#### Dictionary related scripts ####
- Dictionary/dictionary.py: contains the dictionary class which is responsible for all communication with APIs. It also contains the Noun class (represents nouns and their individual properties) and the DictionaryController class (allows for effective retrieval of words from dictionary).

#### Practice and statistics modules ####
- Practice/practice.py: contains a practice controller class which is responsible for all core mechanics regarding the practice modes. It generates questions, checks answers, calls statistics update, etc. .
- Statistics/statistics.py: contains a statistics controller class that is responsible for collecting statistics and saving them appropriately. Currently, it also supports plotting of a graph of accuracy over time.