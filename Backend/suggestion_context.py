import sqlalchemy
from sqlalchemy.orm import relationship, sessionmaker
from suggestion import Base, Suggestion, SuggestionNote
import pentatonic
import random
import operator

"""Database context to access suggestions.
    Should be used with: with SuggestionContext(...) as db:...
"""
class SuggestionContext:
    def __init__(self, address):
        self.db_engine = sqlalchemy.create_engine(address)
        self.DBsession = sessionmaker(bind=self.db_engine)

    def __enter__(self):
        self.session = self.DBsession()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.session.close()
        self.session = None
        if exception_type is not None:
            raise exception_type(exception_value)

    """Returns a random suggestion which belongs to the given key.
    
    Returns:
        Suggestion -- random suggestion which fits to the given key
    """
    def get_random_suggestion(self, key, key_type):
        return self.session.query(Suggestion)\
            .filter(Suggestion.key == key)\
            .filter(Suggestion.key_type == key_type)\
            .order_by(sqlalchemy.sql.expression.func.random())\
            .first()

    """Adds a suggestion to the database.
    """
    def add_suggestion(self, key, key_type, notes, delays, slidings):
        new_suggestion = Suggestion(key=key, key_type=key_type)
        self.session.add(new_suggestion)
        for i in range(len(notes)):
            new_note = SuggestionNote(suggestion=new_suggestion, order=i, note=notes[i],
                                        sliding=slidings[i], delay=delays[i])
            self.session.add(new_note)
        self.session.commit()

    """ Number of available suggestions.
    
    Returns:
        int -- Number of available suggestions
    """
    @property
    def count(self):
        return self.session.query(Suggestion).count()

    """Creates all tables for the database
    """
    def create_database(self):
        Base.metadata.create_all(self.db_engine)

"""Test method which creates 100 random samples.
"""
def populateDatabase(db):
    for i in range(100):
        key = random.randint(0, 11)
        key_type = random.choice(['maj', 'min'])
        if key_type == 'min':
            penta = pentatonic.MinorPentatonic(key)
        else:
            penta = pentatonic.MajorPentatonic(key)
        notes = []
        delays = []
        slidings = []
        for j in range(3):
            notes.append(random.choice(penta.notes))
            delays.append(1)
            slidings.append('N')
        notes.append(random.choice(penta.base_notes))
        delays.append(1)
        slidings.append('N')
        db.add_suggestion(key, key_type, notes, delays, slidings)

"""Test method to test all functionalities
"""
def test():
    with SuggestionContext('sqlite:///test.db') as db:
        db.create_database()
        if db.count == 0:
            populateDatabase(db)
        notes = db.get_random_suggestion(0, 'maj').note_list
        print(notes)
        print(list(map(pentatonic.get_note_name, notes)))

if __name__ == '__main__':
    test()
