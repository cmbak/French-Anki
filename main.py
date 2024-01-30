import argparse
import translators as ts
from reverso_context_api import Client
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import spacy

# Translation
translator = 'bing'
translate_to_lang = 'en'
client = Client('fr', translate_to_lang)

# NLTK
stopwords = set(stopwords.words('french'))
stemmer = SnowballStemmer('french')

# spacy
# py -m spacy download fr_core_news_sm (more eff than dep_news_trf)
nlp = spacy.load('fr_core_news_sm')

# SAMPLE TEXTS FROM LAWLESS FRENCH https://www.lawlessfrench.com
# sample_texts/art_de_la_traduction.txt

parser = argparse.ArgumentParser(description='Convert a piece of French text (utf-8) into Anki cards')
parser.add_argument('filename', nargs=1, help='name of the file to create Anki cards from') # TODO Add multiple file implementation later
args = parser.parse_args()

def validate_file_format(file_path):
    split_file_path = file_path.split('.')
    if len(split_file_path) != 2 or split_file_path[1] != 'txt':
        return False
    return True

def translate_word(word):
    return ts.translate_text(word, translator=translator, from_language='fr', to_language=translate_to_lang)
    # 429 Error w/ Reverso - try word limit?
    # translations = list(client.get_translations(word))
    # if len(translations) < 3:
    #     return translations
    # return translations[:3]

# Prints frequency of (non stopwords) words in a sentence
def print_freq_details(fdist, sent):
    print(sent)
    for word in nlp(sent):
        if fdist[word.text] > 0:
            print(word.text, 'LEMMATIZED', word.lemma_, 'FREQUENCY:', fdist[word.text])
            print(translate_word(word.lemma_), '\n')
    print('=========\n')

def main_prog(filename):
    try:
        with open(filename, encoding="utf-8") as f: # Will only get 1 file
            file = f.read()
            sentences = sent_tokenize(file, language='french')
            words = [word.lower() for word in word_tokenize(file) if word.isalpha() and word not in stopwords]
            fdist = FreqDist(words)
            
            for sent in sentences:
                print_freq_details(fdist, sent)

    except Exception as e:
        print(str(e))
        # TODO quit/throw error instead of printing?

if validate_file_format(args.filename[0]):
    main_prog(args.filename[0])
else:
    print("Please enter a valid file format (.txt)")