import json
import os
import random


def generate_match_data():
    from server import SQLSession
    from fliprBack.models import Match, Playermatch, Player, Day
    session = SQLSession()
    for i in range(5):
        path = './dummy_data/33598{}.json'.format(i+2)
        f = open(path,)
        data = json.load(f)
        match_info = {}
        for key in data['info']:
            if key == 'dates':
                match_info['start_date'] = data['info'][key][0]
            elif key == 'outcome':
                winner = data['info'][key]['winner']
                match_info['winner'] = winner
                try:
                    by_runs = data['info'][key]['by']['runs']
                    match_info['win_by_runs'] = by_runs
                    match_info['win_by_wicket'] = None
                except:
                    by_wickets = data['info'][key]['by']['wickets']
                    match_info['win_by_wicket'] = by_wickets
                    match_info['win_by_runs'] = None
            elif key == 'player_of_match':
                match_info['player_of_match'] = data['info'][key][0]
            elif key == 'teams':
                team1 = data['info'][key][0]
                team2 = data['info'][key][1]
                match_info['team1'] = team1
                match_info['team2'] = team2
            elif key == 'toss':
                toss_winner = data['info'][key]['winner']
                toss_decision = data['info'][key]['decision']
                match_info['toss_winner'] = toss_winner
                match_info['toss_decision'] = toss_decision
            elif key == 'umpires':
                umpires1 = data['info'][key][0]
                umpires2 = data['info'][key][1]
                match_info['umpires1'] = umpires1
                match_info['umpires2'] = umpires2
            elif key == 'overs':
                pass
            else:
                match_info[key] = data['info'][key]
        match_ = Match(
            city=match_info['city'],
            competition=match_info['competition'],
            start_date=match_info['start_date'][0:10],
            gender=match_info['gender'],
            match_type=match_info['match_type'],
            team1=team1,
            team2=team2,
            winner=winner,
            win_by_wicket=match_info['win_by_wicket'],
            win_by_runs=match_info['win_by_runs'],
            player_of_match=match_info['player_of_match'],
            toss_winner=match_info['toss_winner'],
            toss_decision=match_info['toss_decision'],
            umpires1=umpires1,
            umpires2=umpires2,
            venue=match_info['venue']
        )
        dates = Day(
            avail_date=match_info['start_date']
        )
        session.add(match_)
        session.add(dates)
        session.commit()
        m_id = session.query(Match).order_by(Match.id.desc()).first().id
        new_path = './dummy_data/{}.json'.format(m_id)
        os.rename(path, new_path)
        # print(match_info)

        player_set = set()
        for i in data['innings'][0]['1st innings']['deliveries']:
            for ball in i:
                check = ['bowler', 'batsman', 'non_striker']
                for player in i[ball]:
                    if player in check:
                        player_set.add(i[ball][player])
        for i in data['innings'][1]['2nd innings']['deliveries']:
            for ball in i:
                check = ['bowler', 'batsman', 'non_striker']
                for player in i[ball]:
                    if player in check:
                        player_set.add(i[ball][player])
        # print(player_set)
        p_list = open('./dummy_data/pl.json')
        pl = json.load(p_list)
        all_player = []
        for i in pl:
            all_player.append(i)
        while(1):
            if len(player_set) < 22:
                player_set.add(all_player[random.randint(0, 314)])
            else:
                break
        for i in player_set:
            p_id = session.query(Player).filter_by(playername=i).first().id
            playermatch = Playermatch(
                player_id=p_id,
                match_id=m_id
            )
            session.add(playermatch)
        session.commit()
        session.close()
