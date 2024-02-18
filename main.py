import sys
import os
import shutil
import heapq
import translators as ts
import spacy
import genanki
from gtts import gTTS
from anki_note_model import anki_note_model
from SortableNote import SortableNote

# Translation
translator = 'google'
translate_to_lang = 'en'

# spacy
# py -m spacy download fr_core_news_sm (more eff than dep_news_trf)
nlp = spacy.load('fr_core_news_sm')
nlp.add_pipe('sentencizer')
spacy_stopwords = nlp.Defaults.stop_words

# SAMPLE TEXTS FROM LAWLESS FRENCH https://www.lawlessfrench.com

# For anki styling
gender_colour_map = {
    'Masc' : '#80aaff',
    'Fem' : '#ff8080'
}

# TTS Audio deletion
TTS_AUDIO_DIR = 'PY_TTS_AUDIO/' # Safer way to do this?
delete_audio_folder = True

# Returns a tuple - (boolean representing if path/args are valid, appropriate message to be printed)
# NOTE FORMAT OF PATH MATTERS
# Double quotes "" around path if it contains a space
# os.path.exists() throws unicode error if using normal windows path
# So calling this fn will replace the \ with / if user is on windows
def validate_file_format(args):
    if len(args) != 1:
        return (False, 'Please enter a path to the text file')
    
    path = args[0]
    if sys.platform == 'win32':
        path = path.replace('\\', '/')

    if not os.path.exists(path):
        return (False, 'Please enter a valid file path!')
    
    split_path = path.split('.')
    if len(split_path) != 2 or split_path[1].casefold() != 'txt':
        return (False, 'Please enter a valid file format (.txt)!')

    return (True, f'{args[0]} has been found!')

def translate_word(word):
    return ts.translate_text(word, translator=translator, from_language='fr', to_language=translate_to_lang)
    # 429 Error w/ Reverso - try word limit?
    # translations = list(client.get_translations(word))
    # if len(translations) < 3:
    #     return translations
    # return translations[:3]

# Creates an mp3 file of the given word and saves it in directory specified by the var TTS_AUDIO_DIR; returns the path to that file
def create_word_audio(word, media_files):
    tts = gTTS(word, lang='fr')
    genanki_path = f'{word}.mp3'
    path = TTS_AUDIO_DIR + genanki_path
    tts.save(path)
    media_files.append(path)
    return genanki_path

# Creates the directory which temporarily stores the audio files - name of dir is value of TTS_AUDIO_DIR
# This will get deleted after
def create_tts_dir():
    if not os.path.exists(TTS_AUDIO_DIR):
        os.mkdir(TTS_AUDIO_DIR)

# Creates an anki note from a word (spacy token)
# Adds the note to a heap so that the deck will (initially) be in priority order (more frequent words first)
def create_anki_note(word, fdist, heap, media_files):
    word_on_card = word.text
    gender = get_word_token_gender(word)

    # Only want to show lemmatized version of the word if it's different to original version of the word
    # Temp solution for this is to use an empty string
    if word.text.casefold() == word.lemma_.casefold():
        lemmatized_word = ''
    else:
        lemmatized_word = word.lemma_
        word_on_card = word.lemma_

    word_audio_path = create_word_audio(word.text, media_files) # Non-lemmatized version!

    note = SortableNote(anki_note_model, [word.text, lemmatized_word, word.sent.text, translate_word(word.lemma_), word.tag_, gender, f'[sound:{word_audio_path}]'], fdist[word.text], word_on_card) # NOTE: word on card may be different to word in fdist due to lemmatizing
    note.priority *= -1 # Python has no max heap!
    heapq.heappush(heap, note)
    
    del fdist[word.text] # To prevent duplicate cards from being made

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

def create_deck_from_heap(heap, media_files):
    add_heap_to_deck(heap, deck)
    package = genanki.Package(deck)
    package.media_files = media_files
    package.write_to_file('french_gen_py.apkg')
    print("Deck created successfully!")

# Returns dictionary of word:frequency
# Doesn't add different forms of a word to the dictionary
# E.g. importante AND important - only first occurrence is included
def create_freq_dist(words):
    freq_dist = dict()
    for word in words:
        if word.lemma_ in freq_dist:
            freq_dist[word.lemma_] += 1
        elif word.text in freq_dist:
            freq_dist[word.text] += 1
        elif word.text not in freq_dist:
            freq_dist[word.text] = 1
    return freq_dist

# Filters stop words and non alphanumerical characters from text
def process_words(processed_words, sentences):
    for sent in sentences:
        for word in sent:
            if not word.is_stop and word.is_alpha:
                processed_words.append(word)

def main_prog(filename):
    try:
        with open(filename, encoding="utf-8") as f: # Will only get 1 file
            file = f.read()
        # file = re.sub(r'\s+', ' ', file)
        print(f'{filename} has been found...')
    except Exception as e:
        print('Sorry, something went wrong:', str(e))

    media_files = []

    heap = []
    doc = nlp(file)
    sentences = [sent for sent in doc.sents]
    processed_words = [] # spacy tokens

    process_words(processed_words, sentences)

    freq_dist = create_freq_dist(processed_words)
    freq_dist_copy = freq_dist # used for create_anki_note
    create_tts_dir()

    # Creates the anki notes for all the words
    for word in processed_words:
        if word.text in freq_dist: # Don't want the same word to have many cards for its different forms
            create_anki_note(word, freq_dist_copy, heap, media_files)
    
    create_deck_from_heap(heap, media_files)

    if delete_audio_folder:
        try:
            shutil.rmtree(TTS_AUDIO_DIR)
        except PermissionError: # Should (hopefully) only be thrown if get WinError 5 (access is denied)
            print(f'The directory {TTS_AUDIO_DIR} could not be deleted.')
            print("It is safe to delete as the Anki deck has been created and exported successfully.")
            print('Next time, try running this program as an administrator.')

# ==========================================================

args = sys.argv[1:]
is_valid, msg = validate_file_format(args);

if is_valid:
    DECK_ID = 1479086433
    deck = genanki.Deck(DECK_ID, 'FRENCH GEN PY')
    main_prog(args[0])
else:
    print(msg)