import click
from .search import Search

@click.group()
def cli():
    pass

@click.command()
@click.option('--keyword', prompt='keyword', help='keyword to search files from google drive.')
def search(keyword):
    """search file name and id from google drive."""
    Search().search_keyword(keyword)

cli.add_command(search)
