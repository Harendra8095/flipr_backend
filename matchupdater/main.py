import json
import datetime
import time
import redis
import os
from matchupdater.models import *
from matchupdater import create_db_engine, create_db_sessionFactory
from matchupdater.config import DbEngine_config


engine = create_db_engine(DbEngine_config)
SQLSession = create_db_sessionFactory(engine)
print(os.environ.get('REDIS_URL'))
redis_client = redis.from_url(os.environ.get('REDIS_URL'))
redis_client.mset({
    "caught":   25,
    "bowled":	33,
    "run out":	25,
    "lbw":	33,
    "retired hurt":	0,
    "stumped":	25,
    "caught and bowled":	40,
    "hit wicket":	25,
    "Per Run":	1,
    "50 runs scored":	58,
    "100 runs scored":	116
})


def get(key, decode=True):
    """set decode to False when value stored as a string"""
    value = redis_client.get(key)
    if not decode:
        return value
    if value is not None:
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError:
            return value


def livematch(curr_date):
    curr_date = datetime.datetime(2008, 4, 18)
    session = SQLSession()
    connection = session.connection()
    today_ma = session.query(Match).filter_by(start_date=curr_date).first()
    if today_ma == None:
        return
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
    event = open('../dummy_data/{}.json'.format(match_id),)
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
                    player = score['bowler']
                    how = score['wicket']['kind']
                    points = get(how)
                except:
                    pass
                print(player, " ", points)
                session = SQLSession()
                connection = session.connection()
                print(match_id, " ", last_ball)
                prev_score = session.query(Livescore).filter_by(ball=last_ball).join(
                    Livescore.playermatch).filter_by(match_id=match_id).all()
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
    session = SQLSession()
    connection = session.connection()
    prev_score = session.query(Livescore).filter_by(ball=last_ball).join(
        Livescore.playermatch).filter_by(match_id=match_id).all()
    for i in prev_score:
        score_histroy = Scorehistory(
            points=i.points,
            playermatch_id=i.playermatch.id
        )
        session.add(score_histroy)
    today_ma = session.query(Match).filter_by(start_date=curr_date).first()
    today_ma.match_status = 'Finished'
    session.commit()
    session.close()
    connection.close()


if __name__ == "__main__":
    i = 1
    while True:
        session = SQLSession()
        connection = session.connection()
        cur_date = session.query(Day).filter_by(id=i).first().avail_date
        livematch(cur_date)
        i += 1
        time.sleep(7200)
