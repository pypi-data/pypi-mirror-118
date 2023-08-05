import click

@click.command(name='greet')
@click.option('-n', default='World', type=str)
def greet(n):
	click.echo(f"Hello {n}!")
