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


cli.add_command(testdb)


if __name__ == '__main__':
    cli()
