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




cli.add_command(testdb)
cli.add_command(initdb)
cli.add_command(dropdb)


if __name__ == '__main__':
    cli()
