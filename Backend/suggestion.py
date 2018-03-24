import sqlalchemy
from sqlalchemy import Integer, Column, ForeignKey, String
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import operator

Base = declarative_base()

class Suggestion(Base):
    __tablename__ = 'suggestion'
    id = Column(Integer, primary_key=True)
    key = Column(Integer, nullable=False)
    key_type = Column(String(255), nullable=False)
    notes = relationship('SuggestionNote', back_populates='suggestion')

    @property
    def note_list(self):
        s = sorted(self.notes, key=operator.attrgetter('order'))
        return list(map(operator.attrgetter('note'), s))
    
class SuggestionNote(Base):
    __tablename__ = 'suggestion_note'
    suggestion_id = Column(Integer, ForeignKey('suggestion.id'), primary_key=True)
    suggestion = relationship('Suggestion', back_populates='notes')
    order = Column(Integer, primary_key=True)
    note = Column(Integer, primary_key=True)
