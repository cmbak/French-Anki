from genanki import Note

class SortableNote(Note):
    def __init__(self, model, fields, priority):
        super().__init__(model, fields)
        self.priority = priority

    def __eq__(self, other):
        return self.priority == other.priority
    
    def __lt__(self, other):
        return self.priority < other.priority