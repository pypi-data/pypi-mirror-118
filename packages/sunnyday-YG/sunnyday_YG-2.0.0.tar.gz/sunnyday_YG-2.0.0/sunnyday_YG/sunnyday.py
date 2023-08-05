import pprint
import requests


class Weather:
    """Creates a weather object getting an apikey as input
    and either a city name or lat and lon coordinates.

    Package use example:

    # Create a weather object using a city name:
    # The api key below is not guaranteed to work.
    # Get your own apikey from https://openweathermap.org
    # And wait a couple of hours for the apikey to be activated

    >>> weather1 = Weather(apikey = "26631f0f41b95fb9f5ac0df9a8f43c92", city="Addis Ababa")

    # Using latitude and longitude coordinates
    >>> weather2 = Weather(apikey = "26631f0f41b95fb9f5ac0df9a8f43c92", lat=9.025, lon=38.7469)

    # Get complete weathe data for the nexy we hours:
    >>> weather1.next_12h()

    # Simplified data for the next 12 hours:
    >>> weather1.next_12h_simplified()

    Sample url to get sky condition icons:
    https://openweathermap.org/img/wn/10d@2x.png
    """
    def __init__(self, apikey, city=None, lat=None, lon=None, units="metric"):
        self.apikey = apikey
        self.city = city
        self.lat = lat
        self.lon = lon
        self.units = units

        if self.city:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={self.city}&appid={self.apikey}&units={self.units}"
            r = requests.get(url)
            self.data = r.json()
        elif self.lat and self.lon:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={self.lat}&lon={self.lon}" \
                  f"&appid={self.apikey}&units={self.units}"
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError("provide either a city or lat lon arguments")
        if self.data["cod"] != "200":
            raise ValueError(self.data["message"])

    def next_12h(self):
        """ returns 3-hour data for the next 12 hours as dict.
        """
        return self.data['list'][:4]

    def next_12h_simplified(self):
        """returns date, temperature, and sky condition every 3 hours
        for the next 12 hours as a tuple of tuples
        """
        simple_data = []
        for dicty in self.data['list'][:4]:
            simple_data.append((dicty['dt_txt'],
                                dicty['main']['temp'],
                                dicty['weather'][0]['description'],
                                dicty['weather'][0]['icon'],
                                ))
        return simple_data


if __name__ == "__main__":
    weather = Weather(apikey="26631f0f41b95fb9f5ac0df9a8f43c92", city="Addis kAbaba")
    pprint.pprint(weather.next_12h())
    pprint.pprint(weather.next_12h_simplified())
    # weather = Weather(apikey="26631f0f41b95fb9f5ac0df9a8f43c92", lat="40.1", lon="3.4")
    # pprint.pprint(weather.next_12h())
    # weather = Weather(apikey="26631f0f41b95fb9f5ac0df9a8f43c92")
    # pprint.pprint(weather.next_12h())
