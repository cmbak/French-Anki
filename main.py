import argparse
import heapq
import translators as ts
from reverso_context_api import Client
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
# nltk.download('stopwords')
from nltk.corpus import stopwords
import spacy
import genanki

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

parser = argparse.ArgumentParser(description='Convert a piece of French text (utf-8) into Anki cards')
parser.add_argument('filename', nargs=1, help='name of the file to create Anki cards from') # TODO Add multiple file implementation later
args = parser.parse_args()

# For anki styling
gender_colour_map = {
    'Masc' : '#80aaff',
    'Fem' : '#ff8080'
}

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


# TODO Conditional formatting?
anki_note_model = genanki.Model(
    1770821663,
    'PY Sentence Mining Model',
    fields=[
        {'name': 'Word'},
        {'name': 'Sentence'},
        {'name': 'Translation'},
        {'name': 'Tag'},
        {'name': 'Gender'}
    ],
    templates=[
        {
            'name': 'Card PY GEN',
            'qfmt': '<div id="french-word"><b>{{Word}}</b></div><div id="sentence"><br />{{Sentence}}</div>',
            'afmt': '{{FrontSide}}<hr id="answer"><em id="tag">{{Tag}}</em> <b>{{Translation}}<b><div id="gender">{{Gender}}</div>'
        }
    ],
    css='''
        .card {
            padding: 1.5rem;
            font-size: 2.2rem;
            font-family: Arial;
            text-align: center;
        }

        #answer {
            margin: 1rem auto;
        }

        #sentence {
            margin-bottom: 2.5rem;
        }

        #tag {
            color:gray;
            font-size: 1.1rem;
            margin-right: 0.8rem;
        }
        
        #gender {
            font-weight: normal;
        }
        '''
)

# creates anki notes from a sentence
# adds the note to a HEAP so that the deck will be (initially) in priority order (more frequent words first)
def create_anki_note(sentence, fdist, heap):
    doc = [word for word in nlp(sentence) if word.text.isalpha()]

    for word in doc:
        # ensure that word won't have multiple notes
        if fdist[word.text] > 1 or fdist[word.text] == 0: # 0 if stopword or one letter (see main)
            continue

        gender = get_word_token_gender(word)
        note = SortableNote(anki_note_model, [word.text, sentence, translate_word(word.lemma_), word.tag_, gender], fdist[word.text])
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
    deck = genanki.Deck(DECK_ID, 'ANKI LANGUAGE PY')
    add_heap_to_deck(heap, deck)
    genanki.Package(deck).write_to_file('testpy.apkg')
    print("Deck created successfully!")

def main_prog(filename):
    print(f'{filename} has been found...')
    try:
        file = ""
        
        with open(filename, encoding="utf-8") as f: # Will only get 1 file
            file = f.read() 
        
        sentences = sent_tokenize(file, language='french')
        words = [word.lower() for word in word_tokenize(file) if word.isalpha() and word.lower() not in stopwords and len(word)>1]
        fdist = FreqDist(words)
        words = set(words)
        heap = []

        for sent in sentences:
            create_anki_note(sent, fdist, heap)
        
        create_deck_from_heap(heap)

        # TODO need to ensure SET of words

    except Exception as e:
        print('Sorry, something went wrong:', str(e))

if validate_file_format(args.filename[0]):
    main_prog(args.filename[0])
else:
    print("Please enter a valid file format (.txt)")