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


def get_city_woeid(city) -> int:
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
            city_woeid = city_info["cities"]
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


def get_rain_days_on_location(woeid):
    url_format = "{}location/{}/".format(URL_BASE, woeid)
    try:
        response = requests.get(url_format)
        consolidated_weather = response.json()["consolidated_weather"]
        rain_days = [
            (c["applicable_date"], c["weather_state_name"])
            for c in consolidated_weather
            if c["weather_state_abbr"] in ["hr", "s", "lr"]
        ]
        return rain_days
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
def rain_in_future(ctx, city):
    """ if the state of weather in the asking city is the one excepted or not"""

    city_woeid = get_city_woeid(city)
    if not city_woeid:
        city = click.prompt(
            "There is no city with this name. Enter a correct city name"
        )
        ctx.invoke(rain_in_future, city=city)
    rain_days = get_rain_days_on_location(city_woeid)
    if rain_days:
        click.echo("It's going to rain the following days")
        for r in rain_days:
            click.echo("{} : {}".format(r[0], r[1]))
    else:
        click.echo("No rain in the next days")


if __name__ == "__main__":
    main()
