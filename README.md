# Sarnaik_Kunaal_DS3002_DataProject2

*Author*: Kunaal Sarnaik (kss7yy@virginia.edu)<br/>
*Course*: DS 3002 - Data Science Systems (Spring 2021)<br/>
*Date*: May 10th, 2021<br/>
*Professor*: Neal Magee, Ph.D.<br/>
*Project Name*: Air Visual API Twitter Bot<br/>
*Assignment*: DS 3002 Data Project #2<br/>

Welcome to my DS3002: Data Science Systems Data Project #2 repository!

This repository contains the necessary files to write a Dockerized Python3 application that can be run to successfully execute the Twitter API, reading and writing information from the remote, publicly-accessible AirVisual API (https://www.iqair.com/us/air-pollution-data-api). Essentially, the applications creates a Twitter Bot that automatically replies to mentions querying global air quality or weather information via tweets or direct messages (depending on the number of characters present in the response). I created this containerized application to run on an Amazon AWS EC2 Instance, such that responding to mentions is automatic and continuous.

The Twitter Bot (@AirVisualBot; https://twitter.com/AirVisualBot) responds to mentions from Twitter users querying information about the air quality (i.e., pollution) or weather (e.g., temperature, air pressure, humidity, or wind information) in a certain city. The city can be queried using supported cities, states, and countries, or it can be queried using GPS coordinates (latitude and longitude). Using the query as provided by the Bot's mentions on its Twitter feed, the code then retrieves according data from the AirVisual API in order to respond via direct message or tweet reply. It does this using a conditional if-elif-else statement in Python, leveraging the Tweepy Python library that runs in harmony with the Twitter Developer API. Finally, if the user requests help via an according query, enters in a unsupported command, or has their query result in a bad HTTP request to the API, the Bot responds with an informative help message and links to this ReadMe file to aid the user in reconstructing the query.

Please enjoy this project!

- Github Repository: https://github.com/kss7yy/Sarnaik_Kunaal_DS3002_DataProject2
- Docker Container: https://hub.docker.com/r/kss7yy/sarnaik_airvisual_api_twitter_bot
- Twitter Account: https://twitter.com/AirVisualBot
- AirVisual API: https://www.iqair.com/us/air-pollution-data-api

## Twitter Usability

This section outlines a list of supported commands for the Twitter Bot. The usability that is shown in the succeeding sub-sections is what a Twitter user would Tweet in order for the Bot to respond with according information!

Outline of supported functions by the Twitter Bot:

- [Function 0: HELP!!!](#function)
- [Function 1: List of Supported Countries](#function-1-list-of-supported-countries)
- [Function 2: List of Supported States in a Country](#function-2-list-of-supported-states-in-a-country)
- [Function 3: List of Supported Cities in a State and Country](#function-3-list-of-supported-cities-in-a-state-and-country)
- [Function 4: Weather Summary with GPS Coordinates](#function-4-weather-summary-with-gps-coordinates)
- [Function 5: Pollution Summary with GPS Coordinates](#function-5-pollution-summary-with-gps-coordinates)
- [Function 6: Weather Summary with Specified Location](#function-6-weather-summary-with-specified-location)
- [Function 7: Pollution Summary with Specified Location](#function-7-pollution-summary-with-specified-location)
- [Function 8: Temperature with GPS Coordinates](#)
- [Function 9: Temperature with Specified Location](#)
- [Function 10: Air Pressure with GPS Coordinates](#)
- [Function 11: Air Pressure with Specified Location](#)
- [Function 12: Humidity with GPS Coordinates](#)
- [Function 13: Humidity with Specified Location](#)
- [Function 14: Wind Information with GPS Coordinates](#)
- [Function 15: WInd Information with Specified Location](#)

### Function 0: Help


### Function 1: List of Supported Countries

This function allows the user to query the bot for a list of supported countries that the API has air quality and weather information for. The usability of this function is as follows:

```
@AirVisualBot list supported countries
```

From there, the Bot retrieves the supported countries in the AirVisual API using an according GET request to the following endpoint: http://api.airvisual.com/v2/countries?key={{YOUR_API_KEY}}. Here is an example of this request in action:

![d](./images/img_fun1.PNG)

In this case, the response of the request contained too many characters to be tweeted, so the user received a direct message of the supported countries from the Bot:

![d](./images/img_fun1response.PNG)

### Function 2: List of Supported States in a Country

This function allows the user to query the bot for a list of supported states in a country that the API has air quality and weather information for. The usability of this function is as follows:

```
@AirVisualBot list supported states in {{enter-country-name}}
```

From there, the Bot retrieves the supported states in the specified country from the AirVisual API using an according GET request to the following endpoint: http://api.airvisual.com/v2/states?country={{COUNTRY_NAME}}&key={{YOUR_API_KEY}}. Here is an example of this request in action for the states of USA:

![d](./images/img_fun2.PNG)

Similarly, the list of states surpassed the Twitter tweet character limit. Here is the direct message that the user received from the Bot:

![d](./images/img_fun2response.PNG)

### Function 3: List of Supported Cities in a State and Country

This function allows the user to query the bot for a list of supported cities in a supported state and country that the API has air quality and weather information for. The usability of this function is as follows:

```
@AirVisualBot list supported cities in {{enter-state-name}}, {{enter-country-name}}
```

From there, the Bot retrieves the supported cities in the specified state and country from the AirVisual API using an according GET request to the following endpoint: http://api.airvisual.com/v2/cities?state={{STATE_NAME}}&country={{COUNTRY_NAME}}&key={{YOUR_API_KEY}}. Here is an example of this request in action for the cities of California, USA:

![d](./images/img_fun3.PNG)

Again, the list of countries in California surpassed the Twitter tweet character limit. Here is the direct message that the user received from the Bot:

![d](./images/img_fun3response.PNG)

### Function 4: Weather Summary with GPS Coordinates

 This function allows the user to query a current weather summary (temperature, air pressure, humidity, and wind information) pertaining to a city that is supported and nearest the latitude and longitude GPS coordinates specified. The usability of this function is as follows:

 ```
 @AirVisualBot weather summary of lat <<enter-lat-here>> and long <<enter-long-here>>
 ``` 

Please note that the latitude must be specified between -90 and 90 (inclusively), and the longitude must be specified between -180 and 180 (inclusively). From there, the Bot retrieves the weather information in the city nearest to those coordinates from the AirVisual API using an according GET request to the following endpoint: http://api.airvisual.com/v2/nearest_city?lat={{LATITUDE}}&lon={{LONGITUDE}}&key={{YOUR_API_KEY}}. Here is an example of this request in action for the longitude and latitude nearest to Lost Creek, Texas in the United States of America:

![d](./images/img_fun4.PNG)

### Function 5: Pollution Summary with GPS Coordinates

 This function allows the user to query a current pollution summary pertaining to a city that is supported and nearest the latitude and longitude GPS coordinates specified. The maximally concentrated pollutant (e.g., pm2.5, pm10, ozone, nitrogen dioxide, sulfur dioxide, and carbon monoxide) is retrieved as determined by the USA Air Quality Rating. Then, a personalized message based on the rating of that pollutant is also retrieved. The usability of this function is as follows:

 ```
 @AirVisualBot pollution summary of lat <<enter-lat-here>> and long <<enter-long-here>>
 ``` 

Please note that the latitude must be specified between -90 and 90 (inclusively), and the longitude must be specified between -180 and 180 (inclusively). From there, the Bot retrieves the pollution information in the city nearest to those coordinates from the AirVisual API using an according GET request to the following endpoint: http://api.airvisual.com/v2/nearest_city?lat={{LATITUDE}}&lon={{LONGITUDE}}&key={{YOUR_API_KEY}}. Here is an example of this request in action for the longitude and latitude nearest to Lost Creek, Texas in the United States of America:

![d](./images/img_fun5.PNG)

Similar to the first three functions, the user received a direct message since the character limit for twitter was exceeded in the response:

![d](./images/img_fun5response.PNG)

### Function 6: Weather Summary with Specified Location

This function allows the user to query a current weather summary (temperature, air pressure, humidity, and wind information) pertaining to a specified city, state, and country. Note that the supported cities, states, and countries can be found using the first three functions above. The usability of this function is as follows:

 ```
 @AirVisualBot weather summary of <<enter-city-here>>, <<enter-state-here>> in country <<enter-country-here>>
 ``` 

From there, the Bot retrieves the weather information in that specified city from the AirVisual API using an according GET request to the following endpoint: http://api.airvisual.com/v2/city?city={{CITY}}&state={{STATE}}&{{COUNTRY}}=USA&key={{YOUR_API_KEY}}. Here is an example of this request in action for San Francisco, California in country USA:

![d](./images/img_fun6.PNG)

### Function 7: Pollution Summary with Specified Location

This function allows the user to query a current pollution summary pertaining to a specified city, state, and country. Note that the supported cities, states, and countries can be found using the first three functions above. The usability of this function is as follows:

 ```
 @AirVisualBot pollution summary of <<enter-city-here>>, <<enter-state-here>> in country <<enter-country-here>>
 ``` 

From there, the Bot retrieves the pollution information in that specified city from the AirVisual API using an according GET request to the following endpoint: http://api.airvisual.com/v2/city?city={{CITY}}&state={{STATE}}&{{COUNTRY}}=USA&key={{YOUR_API_KEY}}. Here is an example of this request in action for San Francisco, California in country USA:

![d](./images/img_fun7.PNG)

Here is the direct message the user received:

![d](./images/img_fun7response.PNG)

### Function 8: Temperature with GPS Coordinates

### Function 9: Temperature with Specified Location

### Function 10: Air Pressure with GPS Coordinates

### Function 11: Air Pressure with Specified Location

### Function 12: Humidity with GPS Coordinates

### Function 13: Humidity with Specified Location

### Function 14: Wind Information with GPS Coordinates

### Function 15: WInd Information with Specified Location

## Error Handling in Twitter

### Case 1: Bad HTTP Request

### Case 2: Unsupported Command

## Cloning Usability

## Overview of Files

## End Notes