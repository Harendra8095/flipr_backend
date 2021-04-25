from fliprBack.models.userModel import Userteam
from server import SQLSession
from fliprBack.models import *
session = SQLSession()

print("live score table")
prev_score = session.query(Livescore).filter_by(ball=0).join(
    Livescore.playermatch).filter_by(match_id=1).all()
print(prev_score)

# q = session.query(Match).all()
# print("All matches")
# for i in q:
#     print(i.team1)

# q = session.query(Playermatch).filter_by(match_id=3).all()
# print("List of Players in a match")
# userteam_p = []
# for i in q:
#     print(i.player.playername)
#     if len(userteam_p) < 11:
#         userteam_p.append(i.id)

# for i in userteam_p:
#     c_v = session.query(Player).filter_by(id=i).first()
#     mp_q = session.query(Userteam).join(Userteam.playermatch).filter(
#         Userteam.user_id == 6).filter(Playermatch.match_id == 3).count()
#     if mp_q >= 11:
#         print("Team Size full")
#         break
#     my_player = Userteam(
#         user_id=6,
#         playermatch_id=i,
#         credit_bal=c_v.credit_value
#     )
#     session.add(my_player)
#     session.commit()

# mp_q = session.query(Userteam).join(Userteam.playermatch).filter(
#     Userteam.user_id == 6).filter(Playermatch.match_id == 3).all()
# for i in mp_q:
#     print(i.playermatch.player.playername)
