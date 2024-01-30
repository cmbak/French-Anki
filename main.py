import argparse
import translators as ts
from reverso_context_api import Client
import nltk
from nltk.tokenize import sent_tokenize

translate_to_lang = 'en'
client = Client('fr', translate_to_lang)

# SAMPLE TEXTS FROM LAWLESS FRENCH https://www.lawlessfrench.com

parser = argparse.ArgumentParser(description='Convert a piece of French text (utf-8) into Anki cards')
parser.add_argument('filename', nargs=1, help='name of the file to create Anki cards from') # TODO Add multiple file implementation later
args = parser.parse_args()



def validate_file_format(file_path):
    split_file_path = file_path.split('.')
    if len(split_file_path) != 2 or split_file_path[1] != 'txt':
        return False
    return True

def main_prog(filename):
    file = ""

    try:
        with open(filename, encoding="utf-8") as f: # Will only get 1 file
            file = f.read()

            sentences = sent_tokenize(file, language='french')
            for s in sentences:
                print(s, "\nTRANSLATION\n", ts.translate_text(s, translator='bing', from_language='fr', to_language=translate_to_lang), "\n===============\n")            

    except Exception as e:
        print(str(e))
        # TODO quit/throw error instead of printing?

if validate_file_format(args.filename[0]):
    main_prog(args.filename[0])
else:
    print("Please enter a valid file format (.txt)")


# Need to ensure that file is txt file!