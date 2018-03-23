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
    def get_random_suggestion(self, key):
        return self.session.query(Suggestion).order_by(sqlalchemy.sql.expression.func.random()).first()

    """Adds a suggestion to the database.
    """
    def add_suggestion(self, key, notes):
        new_suggestion = Suggestion(key=key)
        self.session.add(new_suggestion)
        for i in range(len(notes)):
            new_note = SuggestionNote(suggestion=new_suggestion, order=i, note=notes[i])
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
        penta = pentatonic.MajorPentatonic(key)
        notes = []
        for j in range(4):
            notes.append(random.choice(penta.notes))
        db.add_suggestion(key, notes)

"""Test method to test all functionalities
"""
def test():
    with SuggestionContext('sqlite:///test.db') as db:
        db.create_database()
        if db.count == 0:
            populateDatabase(db)
        print(db.get_random_suggestion(0).note_list)

if __name__ == '__main__':
    test()
