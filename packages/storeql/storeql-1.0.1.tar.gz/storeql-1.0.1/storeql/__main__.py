import click
from .commands import greetings, storepw, findpw, connection


@click.group(help='CLI tool to store passwords safely (or just a digital vault).')
def cli():
	pass

cli.add_command(greetings.greet)
cli.add_command(storepw.store)
cli.add_command(findpw.finda)

if __name__ == '__main__':
	cli()