import json


def generate_player():
    from server import SQLSession
    from fliprBack.models import Player
    session = SQLSession()
    player_f = open("./dummy_data/pl.json",)
    data = json.load(player_f)
    for i in data:
        player = Player(
            playername=i,
            credit_value=data[i]
        )
        session.add(player)
    session.commit()
    session.close()


def generate_user():
    from server import SQLSession
    import datetime
    from fliprBack.models import User
    session = SQLSession()
    no = 10
    for i in range(no):
        user = User(
            username="user-{}".format(str(i)),
            password="user1234-{}".format(str(i)),
            contact_number='123456789{}'.format(str(i)),
            registered_on=datetime.datetime.utcnow(),
            last_updated_on=datetime.datetime.utcnow(),
            varified=True
        )
        session.add(user)
    session.commit()
    session.close()
