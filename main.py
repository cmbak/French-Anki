# import sys
import argparse
import nltk
from nltk.tokenize import word_tokenize

# SAMPLE TEXTS FROM LAWLESS FRENCH https://www.lawlessfrench.com

parser = argparse.ArgumentParser(description='Convert a piece of French text into Anki cards')
parser.add_argument('filename', nargs=1, help='name of the file to create Anki cards from') # TODO Add multiple file implementation later
args = parser.parse_args()

french_file = args.filename
print(type(french_file))