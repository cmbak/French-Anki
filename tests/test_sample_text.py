import os
import sys
import main
import spacy

def french_anki_dir():
    return os.path.dirname(os.path.dirname(__file__))

def nlp_word(word):
    nlp = spacy.load('fr_core_news_sm')
    return nlp(word)

def nlp_sentence():
    nlp = spacy.load('fr_core_news_sm')
    nlp.add_pipe('sentencizer')
    return [sent for sent in nlp("L’art de la traduction").sents]

# ======== Tests ========

def test_translate_word():
    assert main.translate_word('traduction') == 'translation'

def test_create_tts_dir():
    main.create_tts_dir()
    if sys.platform == 'win32':
        tts_dir = french_anki_dir()+'\\PY_TTS_AUDIO'
    elif sys.platform == 'darwin' or sys.platform == 'linux':
        tts_dir = french_anki_dir()+'/PY_TTS_AUDIO'
    assert os.path.exists(tts_dir) == True

def test_create_word_audio():
    main.create_word_audio('traduction', [])
    if sys.platofrm == 'win32':
        path = french_anki_dir()+'\\PY_TTS_AUDIO\\traduction.mp3'
    elif sys.platform == 'darwin' or sys.platform == 'linux':
        path = french_anki_dir()+'/PY_TTS_AUDIO/traduction.mp3'
    assert os.path.exists(path)

def test_get_word_token_gender():
    doc = nlp_word('traduction')
    for token in doc:
        assert main.get_word_token_gender(token) == 'Fem'

def test_process_words():
    processed_words = []
    main.process_words(processed_words, nlp_sentence())
    art_doc = nlp_word('art')
    traduction_doc = nlp_word('traduction')
    for token in art_doc:
        assert processed_words[0].text == token.text
    for token in traduction_doc:
        assert processed_words[1].text == token.text

def test_create_freq_dist():
    processed_words = []
    main.process_words(processed_words, nlp_sentence())
    assert main.create_freq_dist(processed_words) == {'art': 1, 'traduction': 1}

def test_create_anki_note():
    word = nlp_word('traduction')
    for token in word:
        word_token = token

    processed_words = []
    main.process_words(processed_words, nlp_sentence())
    fdist = main.create_freq_dist(processed_words)
    main.create_anki_note(word_token, fdist, [], [])
    
    assert fdist == {'art': 1}
    
# def test_add_heap_to_deck()
        
# def test_create_deck_from_heap()