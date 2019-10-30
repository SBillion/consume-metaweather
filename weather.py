import click
import requests
import inquirer

__author__ = "Sébastien Billion"
URL_BASE = "https://www.metaweather.com/api/"


@click.group()
def main():
    """
    Simple CLI for checking if it's raining in a city using metaweather API
    """
    pass

def get_city_woeid(city) -> dict:
    """
    Get city woeid from metaweather API
    """
    url_format = URL_BASE + "location/search/"
    query_params = {"query": city}
    city_woeid = None
    try:
        response = requests.get(url_format, params=query_params)
        items = response.json()
        if len(items) > 1:
            cities = [(city["title"], city["woeid"]) for city in items]
            cities_pompted = [
                inquirer.List(
                    "cities",
                    message="Please choose your city in the list",
                    choices=cities,
                )
            ]
            city_info = inquirer.prompt(cities_pompted)
            city_woeid = city_info['cities']
        elif len(items) == 1:
            city_woeid = items[0]["woeid"]
        return city_woeid
    except requests.exceptions.HTTPError as e:
        click.echo("Http Error:", e)
    except requests.exceptions.ConnectionError as e:
        click.echo("Error Connecting:", e)
    except requests.exceptions.Timeout as e:
        click.echo("Timeout Error:", e)
    except requests.exceptions.RequestException as e:
        click.echo("Something goes wrong", e)

def get_weather_on_location(woeid):
    url_format = "{}location/{}/".format(URL_BASE, woeid)
    try:
        response = requests.get(url_format)
        click.echo(response.json())
    except requests.exceptions.HTTPError as e:
        click.echo("Http Error:", e)
    except requests.exceptions.ConnectionError as e:
        click.echo("Error Connecting:", e)
    except requests.exceptions.Timeout as e:
        click.echo("Timeout Error:", e)
    except requests.exceptions.RequestException as e:
        click.echo("Something goes wrong", e)


@main.command()
@click.option("--city", help="The city you want to know if it's raining", prompt="City")
@click.pass_context
def is_it_raining(ctx, city):
    """ if the state of weather in the asking city is the one excepted or not"""

    city_woeid = get_city_woeid(city)
    if not city_woeid:
        city = click.prompt(
            "There is no city with this name. Enter a correct city name"
        )
        ctx.invoke(is_it_raining, city=city)
    click.echo(city_woeid)
    get_weather_on_location(city_woeid)



if __name__ == "__main__":
    main()
