from fliprBack.models.userModel import Userteam
from server import SQLSession
from fliprBack.models import *
session = SQLSession()


prev_score = session.query(Livescore).join(
        Livescore.playermatch).filter(
            Playermatch.match_id==1).filter(
                Livescore.ball==2.1).order_by(
                    Livescore.id.asc()).limit(5)
# print(prev_score)
for i in prev_score:
    print(i.id)

print("live score table")
prev_score = session.query(Livescore).join(
    Livescore.playermatch).filter(
        Livescore.ball==15.2).filter(
            Playermatch.match_id==1).all()
print(prev_score)

q = session.query(Match).all()
print("All matches")
for i in q:
    print(i.team1)

q = session.query(Playermatch).filter_by(match_id=3).all()
print("List of Players in a match")
userteam_p = []
for i in q:
    print(i.player.playername)
    if len(userteam_p) < 11:
        userteam_p.append(i.id)

for i in userteam_p:
    c_v = session.query(Player).filter_by(id=i).first()
    mp_q = session.query(Userteam).join(Userteam.playermatch).filter(
        Userteam.user_id == 6).filter(Playermatch.match_id == 3).count()
    if mp_q >= 11:
        print("Team Size full")
        break
    my_player = Userteam(
        user_id=6,
        playermatch_id=i,
        credit_bal=c_v.credit_value
    )
    session.add(my_player)
    session.commit()

mp_q = session.query(Userteam).join(Userteam.playermatch).filter(
    Userteam.user_id == 6).filter(Playermatch.match_id == 3).all()
for i in mp_q:
    print(i.playermatch.player.playername)

q = session.query(Match).all()
payload = []
for i in q:
    if i.match_status=='Upcoming' or i.match_status=='Finished':
        payload.append(
            {
                "match_id": i.id,
                "start_date": i.start_date,
                "team1": i.team1,
                "team2": i.team2,
                "match_status": i.match_status
            }
        )
    else:
        print(i.match_status)

my_team = session.query(Userteam).join(Userteam.playermatch).filter(
    Userteam.user_id == 1).filter(Playermatch.match_id == 1).all()
p_list = []
for i in my_team:
    p_name = i.playermatch.player.playername
    p_list.append(p_name)
p_l = session.query(Playermatch).filter_by(match_id=1).all()
payload = []
num=0
for i in p_l:
    name = i.player.playername
    if name in p_list:
        pass
    else:
        payload.append(
            {
                "player_id": i.player.id,
                "playername": i.player.playername,
                "credit_value": i.player.credit_value
            }
        )
        num += 1
        print(num)
print(payload)