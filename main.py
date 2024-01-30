# import sys
import argparse
import nltk
from nltk.tokenize import word_tokenize

# SAMPLE TEXTS FROM LAWLESS FRENCH https://www.lawlessfrench.com

parser = argparse.ArgumentParser(description='Convert a piece of French text into Anki cards')
parser.add_argument('filename', nargs=1, help='name of the file to create Anki cards from') # TODO Add multiple file implementation later
args = parser.parse_args()

file = ""

def validate_file_format(file_path):
    split_file_path = file_path.split('.')
    if len(split_file_path) != 2 or split_file_path[1] != 'txt':
        return False
    return True

def main_prog(filename):
    try:
        with open(filename, encoding="utf-8") as f: # Will only get 1 file
            file = f.read()
    except Exception as e:
        print(str(e))
        # TODO quit/throw error instead of printing?

    print(file)

if validate_file_format(args.filename[0]):
    main_prog(args.filename[0])
else:
    print("Please enter a valid file format (.txt)")


# Need to ensure that file is txt file!