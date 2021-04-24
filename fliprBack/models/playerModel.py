from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DateTime, Table, ForeignKeyConstraint, Boolean, Float
from sqlalchemy.orm import relationship
from .meta import Base
from flask_bcrypt import Bcrypt

flask_bcrypt = Bcrypt()


class Player(Base):
    """ Player Model for storing player related details """
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, autoincrement=True)
    playername = Column(String(50), nullable=False, unique=True)
    credit_value = Column(Integer)

    # Relationships
    playermatch = relationship('Playermatch', back_populates='player')


class Playermatch(Base):
    """ Many_Player_Plays_in_Many_Matches """
    __tablename__ = "playermatch"

    id = Column(Integer, primary_key=True, autoincrement=True)

    player_id = Column(Integer, ForeignKey('player.id'))
    match_id = Column(Integer, ForeignKey('match.id'))

    # Relationships
    match = relationship('Match', back_populates='playermatch')
    player = relationship('Player', back_populates='playermatch')
    userteam = relationship('Userteam', back_populates='playermatch')
