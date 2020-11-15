parsedResponse['coord']['lon'] --> City geo-location, longitude
parsedResponse['coord']['lat'] --> City geo-location, latitude
parsedResponse['weather']['id'] --> Weather condition id
parsedResponse['weather']['main'] --> Group of weather parameters (Rain, Snow, Extreme etc.)
parsedResponse['weather']['description'] --> Weather condition within the group. You can get the output in your language. Learn more
parsedResponse['weather']['icon'] --> Weather icon id

parsedResponse['main']['temp'] --> Temperature. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.
parsedResponse['main']['feels_like'] --> Temperature. This temperature parameter accounts for the human perception of weather. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.
parsedResponse['main']['pressure'] --> Atmospheric pressure (on the sea level, if there is no sea_level or grnd_level data), hPa
parsedResponse['main']['humidity'] --> Humidity, %
parsedResponse['main']['temp_min'] --> Minimum temperature at the moment. This is minimal currently observed temperature (within large megalopolises and urban areas). Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.
parsedResponse['main']['temp_max'] --> Maximum temperature at the moment. This is maximal currently observed temperature (within large megalopolises and urban areas). Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.
parsedResponse['main']['sea_level'] --> Atmospheric pressure on the sea level, hPa
parsedResponse['main']['grnd_level'] --> Atmospheric pressure on the ground level, hPa
parsedResponse['wind']['speed'] --> Wind speed. Unit Default: meter/sec, Metric: meter/sec, Imperial: miles/hour.
parsedResponse['wind']['deg'] --> Wind direction, degrees (meteorological)
parsedResponse['wind']['gust'] --> Wind gust. Unit Default: meter/sec, Metric: meter/sec, Imperial: miles/hour
parsedResponse['clouds']['all'] --> Cloudiness, %
parsedResponse['rain']['1h'] --> Rain volume for the last 1 hour, mm
parsedResponse['rain']['3h'] --> Rain volume for the last 3 hours, mm
parsedResponse['snow']['1h'] --> Snow volume for the last 1 hour, mm
parsedResponse['snow']['3h'] --> Snow volume for the last 3 hours, mm
parsedResponse['dt'] --> dt Time of data calculation, unix, UTC
parsedResponse['sys']['country'] --> Country code (GB, JP etc.)
parsedResponse['sys']['sunrise'] --> Sunrise time, unix, UTC
parsedResponse['sys']['sunset'] --> Sunset time, unix, UTC
parsedResponse['timezone'] --> timezone Shift in seconds from UTC
parsedResponse['id'] --> id City ID
parsedResponse['name'] --> name City name


# *RULES*
- watch for Response from API when your account is suspended

```
{ "cod": 429,
"message": "Your account is temporary blocked due to exceeding of requests limitation of your subscription type.
Please choose the proper subscription http://openweathermap.org/price"
}
```
- call API no more than one time for every 10 minutes for one location, however you call it by city, geographical coordinates or by zip code. weather model is not updated more frequently than one time per about 10 minutes.
- get a precise geocoding searching result would rather call API by city ID. You can always call API by city name, city coordinates or zip code but the searching result might be a bit less unambiguous.

- If you do not receive a response from the API due to this limitation, please, wait at least for 10 min and then repeat your request.

# Get current Weather for a specified city by name (state and country are optional)
    * Please note that searching by states available only for the USA locations.

```
# city name only
api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
# city name and state
api.openweathermap.org/data/2.5/weather?q={city name},{state code}&appid={API key}
# city name, state, country code
api.openweathermap.org/data/2.5/weather?q={city name},{state code},{country code}&appid={API key}
```

Parameters:
    Required:
        q: City name, state code and country code divided by comma, use ISO 3166 country codes.
        appid: Your unique API key (you can always find it on your account page under the "API key" tab)
    Optional:
        mode: Response format. JSON by default. Possible values are xml and html.
        units: Units of measurement. standard units will be applied by default. Possible values are standard, metric and imperial units are available.
        lang: You can use this parameter to get the output in your language. Learn more


# Get current Weather for a specified city by city id
    * recommended

```
api.openweathermap.org/data/2.5/weather?id={city id}&appid={API key}
```
Parameters:
    Required:
        id: City ID. List of city ID 'city.list.json.gz' can be downloaded here.
        appid: Your unique API key (you can always find it on your account page under the "API key" tab)
    Optional:
        mode: Response format. JSON by default. Possible values are xml and html.
        units: Units of measurement. standard units will be applied by default. Possible values are standard, metric and imperial units are available.
        lang: You can use this parameter to get the output in your language. Learn more

# Get current Weather by lat/long

```
api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
```

Parameters:
    Required:
        lat,lon: longitude and latitude
        appid: Your unique API key (you can always find it on your account page under the "API key" tab)
    Optional:
        mode: Response format. JSON by default. Possible values are xml and html.
        units: Units of measurement. standard units will be applied by default. Possible values are standard, metric and imperial units are available.
        lang: You can use this parameter to get the output in your language. Learn more

# Get current Weather by zip code
    * defaults to USA if no country specified

```
api.openweathermap.org/data/2.5/weather?zip={zip code},{country code}&appid={API key}
```

Parameters:
    Required:
        Zip: Zip code
        appid: Your unique API key (you can always find it on your account page under the "API key" tab)
    Optional:
        mode: Response format. JSON by default. Possible values are xml and html.
        units: Units of measurement. standard units will be applied by default. Possible values are standard, metric and imperial units are available.
        lang: You can use this parameter to get the output in your language. Learn more