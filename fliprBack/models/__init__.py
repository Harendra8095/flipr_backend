from .meta import Base
from .userModel import User, Userteam
from .matchModel import Match, Livescore, Day, Scorehistory
from .playerModel import Player, Playermatch

def createTables(engine):
    # print("Binding")
    print(Base.metadata.tables.keys())
    Base.metadata.bind = engine
    # print("binding done")
    Base.metadata.create_all(engine)


def destroyTables(engine):
    Base.metadata.drop_all(engine)