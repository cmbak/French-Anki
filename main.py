import sys
import os
# import argparse
import heapq
import translators as ts
from reverso_context_api import Client
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
# nltk.download('stopwords')
from nltk.corpus import stopwords
import spacy
import genanki
import re

from anki_note_model import anki_note_model
from SortableNote import SortableNote

# Translation
translator = 'google'
translate_to_lang = 'en'
client = Client('fr', translate_to_lang)

# NLTK
# NOTE - NLTK only has french tagger - could try changing to using spacy only
stopwords = set(stopwords.words('french'))

# spacy
# py -m spacy download fr_core_news_sm (more eff than dep_news_trf)
nlp = spacy.load('fr_core_news_sm')

# SAMPLE TEXTS FROM LAWLESS FRENCH https://www.lawlessfrench.com
# sample_texts/art_de_la_traduction.txt

# parser = argparse.ArgumentParser(description='Convert a piece of French text (utf-8) into Anki cards')
# parser.add_argument('filename', nargs=1, help='name of the file to create Anki cards from') # TODO Add multiple file implementation later

# For anki styling
gender_colour_map = {
    'Masc' : '#80aaff',
    'Fem' : '#ff8080'
}

# Returns a tuple - (boolean representing if path/args are valid, appropriate message to be printed)
# NOTE FORMAT OF PATH MATTERS
# Windows: Double quotes "" around path
# os.path.exists() throws unicode error if using normal windows path
# calling this fn will replace the \ with / if user is on windows
def validate_file_format(args):
    if len(args) > 1 or len(args) == 0:
        return (False, 'Please enter')
    path = args[0]
    if sys.platform == 'win32':
        path = path.replace('\\', '/')
    #print('path', path, sys.platform, os.path.exists(path))
    if not os.path.exists(path):
        return (False, 'Please enter a valid file path!')
    # # TODO VALIDATE THAT IT'S A TEXT FILE!
    # # TODO FIX VALIDATION!
    return (True, f'{args[0]} has been found!')

def translate_word(word):
    return ts.translate_text(word, translator=translator, from_language='fr', to_language=translate_to_lang)
    # 429 Error w/ Reverso - try word limit?
    # translations = list(client.get_translations(word))
    # if len(translations) < 3:
    #     return translations
    # return translations[:3]

# Returns t/f depending on if there's been a note created with the same word already
# E.g. importante (f) will return false if a note has been created with important (m) on it
# Bit inefficient!
def check_if_note_exists(heap, word):
    if len(word.lemma_) > 1:
        for note in heap:
            if note.word_on_card and word.lemma_ == note.word_on_card:
                print(f'A note with {word.lemma_} already exists - not adding {word.text}')
                return True
    return False

# creates anki notes from a sentence
# adds the note to a HEAP so that the deck will be (initially) in priority order (more frequent words first)
def create_anki_note(sentence, fdist, heap):
    doc = [word for word in nlp(sentence) if word.text.isalpha()]

    for word in doc:
        # ensure that word won't have multiple notes
        if fdist[word.text] > 1 or fdist[word.text] == 0 or check_if_note_exists(heap, word): # 0 if stopword or one letter (see main)
            continue

        word_on_card = word.text
        gender = get_word_token_gender(word)

        # Only want to show lemmatized version of the word if it's different to original version of the word
        # Temp solution for this is to use an empty string
        if word.text.casefold() == word.lemma_.casefold():
            lemmatized_word = ''
        else:
            lemmatized_word = word.lemma_
            word_on_card = word.lemma_

        note = SortableNote(anki_note_model, [word.text, lemmatized_word, sentence, translate_word(word.lemma_), word.tag_, gender], fdist[word.text], word_on_card) # NOTE: word on card may be different to word in fdist due to lemmatizing
        note.priority *= -1 # Python has no max heap!
        heapq.heappush(heap, note)

def add_heap_to_deck(heap, deck):
    while len(heap) > 0:
        note = heapq.heappop(heap)
        deck.add_note(note)

# word is of type Token (from spacy)
def get_word_token_gender(word):
    gender = word.morph.get('Gender') # E.g. Returns ['Male']
    if len(gender) != 0:
        return gender[0]
    return ''

def create_deck_from_heap(heap):
    DECK_ID = 1479086433
    deck = genanki.Deck(DECK_ID, 'ANKI LANGUAGE SPACY PY')
    add_heap_to_deck(heap, deck)
    genanki.Package(deck).write_to_file('testpy.apkg')
    print("Deck created successfully!")

def main_prog(filename):
    print(f'{filename} has been found...')
    try:
        file = ""
        
        with open(filename, encoding="utf-8") as f: # Will only get 1 file
            file = f.read()

        file = re.sub(r'\s+', ' ', file)
        
        sentences = sent_tokenize(file, language='french')
        words = [word.lower() for word in word_tokenize(file) if word.isalpha() and word.lower() not in stopwords and len(word)>1]
        fdist = FreqDist(words)
        words = set(words)
        heap = []
        
        # lemmatized_words_added = set()

        # spacy_doc = nlp(file)
        # spacy_words = {token.lemma_ for token in spacy_doc if token.is_stop == False and token.is_punct == False and token.text.startswith("-") == False}
        # print(spacy_words)

        for sent in sentences:
            create_anki_note(sent, fdist, heap)
        
        create_deck_from_heap(heap)

    except Exception as e:
        print('Sorry, something went wrong:', str(e))

args = sys.argv[1:]
is_valid, msg = validate_file_format(args);
if is_valid:
    print(f'{args[0]} is a valid file! SPLIT:{args[0].split('.txt')} {args[0].split('.')}')
    # main_prog(args[0])
else:
    print(msg)