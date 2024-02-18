# French Gen Python
## Description

FRENCH GEN PYTHON is a Python script which allows you to turn a piece of french text into Anki flashcards.

## Requirements

- [Python](https://www.python.org/downloads/) (>=3.8)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Anki](https://apps.ankiweb.net/)

## Installation

1. Clone this repo
```bash
git clone https://github.com/cmbak/French-Anki.git
```
2. Install the required packages using pip
```bash
cd French Anki
pip install requirements.txt
```

## Usage
1. Follow the installation instructions then run the command: 
```bash
py main.py [path]
```
Where path is the FULL path to the .txt file containing the french text.

2. Delete the newly created folder ```PY_TTS_AUDIO/``` if it was not deleted by the program.

3. Import the generated Anki deck (```french_gen_py.apkg```) by opening Anki and going to File>Import and then choose the new deck.
4. Start revising!

### IMPORTANT USAGE NOTES:
- Enter the full path to the file e.g. ```C:\Users\user\Desktop\french_recipe.txt```, not ```./french_recipe.txt```
- Wrap the path in double quotes if there is a space in the path e.g. ```"C:\Users\user\Desktop\Language Learning\some_french_text.txt"```
- The specified file must be a text file (.txt) encoded using UTF-8

### Example:
Using the sample text as an example:
```bash
py main.py "C:\Users\user\Desktop\Language Learning\sample_texts\art_de_la_traduction.txt"
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
