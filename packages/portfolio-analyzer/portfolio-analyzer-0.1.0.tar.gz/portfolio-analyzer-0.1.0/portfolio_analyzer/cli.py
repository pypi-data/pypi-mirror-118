import click

@click.group()
def cli():
    pass


@cli.command()
@click.option('--path', help='path to the CSV file with data')
def summary(path):
    click.echo(path)

@cli.command()
@click.option('--path', help='path to the CSV file with data')
@click.option('--tickers', default="", help='filter to only these tickers, leave empty for all')
def details(tickers):
    click.echo(tickers)


def main():
    cli()