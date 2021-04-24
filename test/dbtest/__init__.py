from test.dbtest.matchdata.matchdata import generate_match_data
from test.dbtest.user_player.u_p_data import generate_player, generate_user


def populate_dummy():
    generate_player()
    generate_user()
    generate_match_data()
