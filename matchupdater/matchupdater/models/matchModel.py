from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DateTime, Table, ForeignKeyConstraint, Boolean, Float
from sqlalchemy.orm import relationship
from .meta import Base
from flask_bcrypt import Bcrypt

flask_bcrypt = Bcrypt()


class Match(Base):
    """ Match Model for storing match related details """
    __tablename__ = "match"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(128))
    competition = Column(String(128))
    start_date = Column(DateTime, nullable=False)
    gender = Column(String(128))
    match_type = Column(String(128))
    team1 = Column(String(256))
    team2 = Column(String(256))
    winner = Column(String(256))
    win_by_wicket = Column(Integer)
    win_by_runs = Column(Integer)
    player_of_match = Column(String(256))
    toss_winner = Column(String(256))
    toss_decision = Column(String(128))
    umpires1 = Column(String(256))
    umpires2 = Column(String(256))
    venue = Column(String(256))
    match_status = Column(String(128))

    # Relationships
    playermatch = relationship('Playermatch', back_populates='match')


class Livescore(Base):
    """ Storing each ball event """
    __tablename__ = "livescore"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ball = Column(Float)
    points = Column(Integer)
    playermatch_id = Column(Integer, ForeignKey('playermatch.id'))

    # Relationships
    playermatch = relationship('Playermatch', back_populates='livescore')


class Day(Base):
    """ Stroing available date """
    __tablename__ = "day"

    id = Column(Integer, primary_key=True, autoincrement=True)
    avail_date = Column(DateTime, nullable=False)
