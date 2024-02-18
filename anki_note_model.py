from genanki import Model

# TODO Conditional formatting?
anki_note_model = Model(
    1770821663,
    'PY Sentence Mining Model',
    fields=[
        {'name': 'Word'},
        {'name': 'LemmatizedWord'},
        {'name': 'Sentence'},
        {'name': 'Translation'},
        {'name': 'Tag'},
        {'name': 'Gender'},
        {'name': 'MyMedia'},
    ],
    templates=[
        {
            'name': 'Card PY GEN',
            'qfmt': '<div id="french-word"><b>{{Word}}</b> {{LemmatizedWord}}</div><div id="sentence"><br />{{Sentence}}</div>{{MyMedia}}',
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