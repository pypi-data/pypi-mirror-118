# Weather Forecast Package python
 Weather Forecast Package python

Creates a weather object getting an apikey as input and either a city name or lat and lon coordinates.

    install pakake using
    >>> pip install sunnyday-YG

    import pakake using
    >>> from sunnyday_YG.sunnyday import Weather

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
 
