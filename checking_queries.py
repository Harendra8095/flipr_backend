from fliprBack.models.userModel import Userteam
from server import SQLSession
from fliprBack.models import *
session = SQLSession()


session.query(Scorehistory).delete()
session.commit()
session.close()

# prev_score = session.query(Livescore).join(
#         Livescore.playermatch).filter(
#             Playermatch.match_id==1).filter(
#                 Livescore.ball==2.1).order_by(
#                     Livescore.id.asc()).limit(5)
# # print(prev_score)
# for i in prev_score:
#     print(i.id)

# print("live score table")
# prev_score = session.query(Livescore).join(
#     Livescore.playermatch).filter(
#         Livescore.ball==15.2).filter(
#             Playermatch.match_id==1).all()
# print(prev_score)

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
