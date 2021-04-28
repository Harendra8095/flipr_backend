import json
import datetime
import time
from matchupdaterBack.models import *


def livematch(m_id):
    from main import redis_client, SQLSession, get
    session = SQLSession()
    connection = session.connection()
    today_ma = session.query(Match).filter_by(id=m_id).first()
    if today_ma == None or today_ma.match_status == 'Finished':
        print("Match not found or maybe already finished")
        return
    session.query(Livescore).delete()
    today_ma.match_status = 'Running'
    match_id = today_ma.id
    redis_client.set(match_id, 0)
    # Update score of players to zero
    init_score = session.query(Playermatch).filter_by(match_id=match_id).all()
    for i in init_score:
        liv_score = Livescore(
            ball=0,
            points=0,
            playermatch_id=i.id
        )
        session.add(liv_score)
    session.commit()
    session.close()
    connection.close()
    event = open('./dummy_data/{}.json'.format(match_id),)
    data = json.load(event)
    time.sleep(5)
    for i in range(2):
        if i:
            inning = '2nd innings'
        else:
            inning = '1st innings'
        for i in data['innings'][i][inning]['deliveries']:
            for next_ball in i:
                last_ball = get(match_id)
                score = i[str(next_ball)]
                player = score['batsman']
                points = score['runs']['total']
                try:
                    how = score['wicket']['kind']
                    player = score['bowler']
                    points = get(how)
                except:
                    pass
                print(player, " ", points)
                session = SQLSession()
                connection = session.connection()
                print(match_id, " ", last_ball)
                prev_score = session.query(Livescore).join(
                    Livescore.playermatch).filter(
                        Playermatch.match_id==match_id).filter(
                            Livescore.ball==last_ball).order_by(
                                Livescore.id.desc()).limit(22)
                for i in prev_score:
                    if i.playermatch.player.playername == player:
                        add_p = i.points+points
                    else:
                        add_p = i.points
                    liv_score = Livescore(
                        ball=next_ball,
                        points=add_p,
                        playermatch_id=i.playermatch.id
                    )
                    session.add(liv_score)
                session.commit()
                session.close()
                connection.close()
                # Update last ball
                redis_client.set(match_id, float(next_ball))
                time.sleep(5)
    event.close()
    redis_client.set(match_id, 0)
    session = SQLSession()
    connection = session.connection()
    print(last_ball)
    prev_score = session.query(Livescore).join(
        Livescore.playermatch).filter(
            Playermatch.match_id==match_id).filter(
                Livescore.ball==last_ball).order_by(
                    Livescore.id.desc()).limit(22)
    for i in prev_score:
        score_histroy = Scorehistory(
            points=i.points,
            playermatch_id=i.playermatch.id
        )
        session.add(score_histroy)
    today_ma = session.query(Match).filter_by(id=m_id).first()
    today_ma.match_status = 'Finished'
    session.query(Livescore).delete()
    session.commit()
    connection.close()
    session.close()
