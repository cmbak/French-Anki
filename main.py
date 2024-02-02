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

# doc_word is the result of calling nlp on the sentence
def create_anki_card(doc_word, sentence):
    note = genanki.Note(model=anki_note_model, fields=[])

# Prints frequency of (non stopwords) words in a sentence
def print_freq_details(fdist, sent):
    print(sent)
    for word in nlp(sent):
        if fdist[word.text] > 0:
            # print(word.text, 'LEMMATIZED', word.lemma_, 'TAGGED', word.tag_, 'FREQUENCY:', fdist[word.text])
            # print(translate_word(word.lemma_), '\n')
            create_anki_card(word, sent)
    print('=========\n')

# word is of type Token (from spacy)
def get_word_token_gender(word):
    gender = word.morph.get('Gender') # E.g. Returns ['Male']
    if len(gender) != 0:
        return gender[0]
    return ''

# use a max heap :)

def test(fdist, sent):
    deck_id = 1479086433
    deck = genanki.Deck(deck_id, 'ANKI LANGUAGE PY')
    doc = [word for word in nlp(sent) if word.text.isalpha()]

    heap = []

    for word in doc:
        # TODO ENSURE ALPHANUMERIC
        # TODO Conditional formatting in python?
        gender = get_word_token_gender(word)
        note = SortableNote(anki_note_model, [word.text, sent, translate_word(word.lemma_), word.tag_, gender], fdist[word.text])
        note.priority *= -1 # Python has no max heap!
        heapq.heappush(heap, note)

    # add heap to deck
    while len(heap) > 0:
        note = heapq.heappop(heap)
        deck.add_note(note)

    genanki.Package(deck).write_to_file('testpy.apkg')

def main_prog(filename):
    try:
        file = ""
        with open(filename, encoding="utf-8") as f: # Will only get 1 file
            file = f.read() 
        sentences = sent_tokenize(file, language='french')
        words = [word.lower() for word in word_tokenize(file) if word.isalpha() and word not in stopwords]
        fdist = FreqDist(words)
            
        # for sent in sentences:
            # print_freq_details(fdist, sent)
            
        # need to ensure SET of words
        test(fdist, sentences[2])

    except Exception as e:
        print('Sorry, something went wrong:', str(e))
        # TODO quit/throw error instead of printing?

if validate_file_format(args.filename[0]):
    main_prog(args.filename[0])
    # FIXME is this slow?
else:
    print("Please enter a valid file format (.txt)")