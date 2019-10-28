import click
import requests

__author__ = "Sébastien Billion"
URL_BASE = "https://www.metaweather.com/api/"

@click.group()
def main():
    """
    Simple CLI for checking if it's raining in a city using metaweather API
    """
    pass


@main.command()
@click.argument('query')
def search(query):
    """This search and return results corresponding to the city"""
    url_format = URL_BASE + 'location/search/'
    query = "+".join(query.split())

    query_params = {
        'query': query
    }

    response = requests.get(url_format, params=query_params)

    click.echo(response.json())

if __name__ == '__main__':
    main()