def generate_points_data():
    from server import redis_client
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
        "100 runs scored":	116,
        "match_id": 1
    })