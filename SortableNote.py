from genanki import Note

class SortableNote(Note):
    def __init__(self, model, fields, priority, word_on_card):
        super().__init__(model=model, fields=fields)
        self.priority = priority
        self.word_on_card = word_on_card

    def __eq__(self, other):
        return self.priority == other.priority
    
    def __lt__(self, other):
        return self.priority < other.priority