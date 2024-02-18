# French Gen Python
## Description

French Gen Python (name is a wip!) is a Python program which allows you to turn a piece of French text into Anki flashcards.
- The specified text is filtered out to remove punctuation or words which may not be useful to turn into flashcards
  - For example, 'stopwords' such as 'la', 'ci' or 'de' may not be made into flashcards
- Anki flashcards are then made for all of the remaining words
  - On the front of each flashcard there is the the word, the TTS audio of word and the sentence in which the word was originally in
  - On the back of each flashcard there is the translation of the word and the gender of the word if the word is a noun
 
### This produces a flashcard similar to this:

![image](https://github.com/cmbak/French-Anki/assets/17798932/b842d55d-bdce-49ef-b858-8633dbee2108)

## Requirements

- [Python](https://www.python.org/downloads/) (>=3.9)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Anki](https://apps.ankiweb.net/)

## Installation

1. Clone this repo
```bash
git clone https://github.com/cmbak/French-Anki.git
```
2. Navigate to the French-Anki folder and install the required packages using pip
```bash
cd French-Anki
python -m pip install -r requirements.txt
```

## Usage
1. Follow the installation instructions then run the command: 
```bash
python main.py [path]
```
Where path is the FULL path to the .txt file containing the french text.

2. Delete the newly created folder ```PY_TTS_AUDIO/``` if it was not deleted by the program.

3. Import the generated Anki deck (```french_gen_py.apkg```) by opening Anki and going to File>Import and then choose the new deck.
![image](https://github.com/cmbak/French-Anki/assets/17798932/6a4eea6c-a842-47cc-97d9-de7f38e33b50)
4. Start revising :)

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
