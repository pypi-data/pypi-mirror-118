import click
from .search import Search
from .auth import Auth

@click.group()
def cli():
    pass

@click.command()
@click.option('--keyword', prompt='keyword', help='keyword to search files from google drive.')
def search(keyword):
    """search file name and id from google drive."""
    Search().search_keyword(keyword)

@click.command()
def login():
    """login with google account."""
    Auth().login()

cli.add_command(search)
cli.add_command(login)
