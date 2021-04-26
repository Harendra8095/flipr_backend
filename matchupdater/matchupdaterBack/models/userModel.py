from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DateTime, Table, ForeignKeyConstraint, Boolean, Float
from sqlalchemy.orm import relationship
from .meta import Base
from flask_bcrypt import Bcrypt
import datetime

flask_bcrypt = Bcrypt()


class User(Base):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password_hash = Column(String(100), nullable=False)
    contact_number = Column(String(10), nullable=False, unique=True)

    varified = Column(Boolean, nullable=False, default=False)
    registered_on = Column(DateTime, nullable=False)
    last_updated_on = Column(DateTime, nullable=False)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)


class Userteam(Base):
    """ Storing team created by user """
    __tablename__ = "userteam"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    playermatch_id = Column(Integer, ForeignKey('playermatch.id'))
    captain = Column(Boolean)
    vice_captain = Column(Boolean)
    credit_bal = Column(Integer)

    # Relationships
    playermatch = relationship('Playermatch', back_populates='userteam')
