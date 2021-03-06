import click


@click.group()
def cli():
    '''Welcome the to cli for managing Server'''
    pass


@click.command()
def testdb():
    from test.dbtest import populate_dummy
    click.echo("Populating User and Player data")
    populate_dummy()

@click.command()
def initdb():
    from server import engine, createTables
    createTables(engine)
    click.echo('Initialized the database')


@click.command()
def dropdb():
    from server import engine, destroyTables
    destroyTables(engine)
    click.echo('Dropped the database')

@click.command()
def restart():
    from server import clearlivetable, redis_client, SQLSession
    from fliprBack.models  import Scorehistory
    import redis
    session = SQLSession()
    clearlivetable()
    redis_client.flushall()
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
    session.query(Scorehistory).delete()
    session.commit()
    session.close()



cli.add_command(testdb)
cli.add_command(initdb)
cli.add_command(dropdb)
cli.add_command(restart)


if __name__ == '__main__':
    cli()
