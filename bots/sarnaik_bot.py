#!/usr/bin/env python
'''
Name: Kunaal Sarnaik (kss7yy@virginia.edu)
Course: DS 3002 - Data Science Systems (Spring 2021)
Date: May 10th, 2021
Professor: Neal Magee, Ph.D.
Project Name: Air Visual API Twitter Bot
Assignment: DS3002 Data Project #2

File Name: sarnaik_bot.py
File Purpose: Actual code used in order for Twitter Bot to Run!

Github Repository: https://github.com/kss7yy/Sarnaik_Kunaal_DS3002_DataProject2
Docker Container:
Twitter Profile: https://twitter.com/AirVisualBot
AirVisual API: https://www.iqair.com/us/air-pollution-data-api
'''

# Python modules and libraries needed for full functionality of this executable
import tweepy                   # Python library for accessing Twitter's developer API
import requests                 # Python library for performing HTTP Requests (used with the AirVisual REST API)
import logging                  # Standard python module to emit log messages from this executable
import time                     # Standard python module for recording time (used for sleep timer in between runs of code)
import json                     # Standard python module for encoding and decoding JSON data
import os                       # Standard python module for accessing environment variables in the operating system
from config import create_api   # Imports the create_api() function from the config.py executable, which is also included in the Github Repo under the 'bots' directory

# Uses the logging Python module to inform errors and information messages that can help debug issues when they arise. Logs to console with time.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Global variable in order to establish a line break for formatting of text later on in this script.
new_line = "\n\n"

# info_formatter() method to format JSON data retrieved as dictionaries/lists to strings with 'and' placed in
#   s - the dictionary that needs to be turned into a string
#   length - the length of the dictionary passed in from the JSON data
#   
#   Description: Method strips the last comma and leading space. If the length of the dictionary is more than one, and 'and' is placed in and the last comma is stripped. Otherwise, the string is unchanged after the trailing comma and leading space is stripped.
def info_formatter(s, length):
    s = s.rstrip(',')
    s = s.lstrip()
    if length > 1:
        last_comma = s.rindex(',', 0, len(s))
        s = s[:last_comma] + " and" + s[last_comma+1:]
    return s

# extract_list_dict_values() method to transform a dictionary into a list from the JSON data retrieved from AirVisuals API
#   d - the dictionary that must be reformatted into a list
#
#   Description: Method iterates through the dictionary and then appends each value in the dictionary to the list; the list is then returned from the method.
def extract_list_dict_values(d):
    values = []
    for ele in d:
        for key in ele.keys() :
            values.append(ele[key])
    return values

# list_to_string() method to transform a list into a long string containing the comma-separated elements of the list in string format
#   l - the list that must be reformatted into a string
#
#   Description: Method traverses through each item of the list and adds them to a growing string with commas in between; the string is then returned from the method.
def list_to_string(l):
    s = ""
    for item in l:
        s += " " + item + ","
    return s

# get_cardinal_direction() method to transform a float degree value to a cardinal direction. This is specifically utilized for the wind information obtained from the AirVisual API to transform arbitrary degree values into cardinal directions (N, E, S, W, etc.)
#   deg - the degree value to be transformed into a cardinal direction
#
#   Description: Method uses a if-elif-else conditional statement to transform the degree value (float) into a cardinal direction (string). N represents 0 degrees. E represents 90 degrees. S represents 180 degrees. and W represents 270 degrees.
def get_cardinal_direction(deg):
    if deg == 0 or deg == 360:
        cardinal_direction = "N"
    elif deg < 90:
        cardinal_direction = "NE"
    elif deg == 90:
        cardinal_direction = "E"
    elif deg < 180:
        cardinal_direction = "SE"
    elif deg == 180:
        cardinal_direction = "S"
    elif deg < 270:
        cardinal_direction = "SW"
    elif deg == 270:
        cardinal_direction = "W"
    else:
        cardinal_direction = "NW"
    return cardinal_direction

# get_supported_countries() method to return the list of supported countries in the AirVisual API
#   base_url - The base URL address that is built upon for the AirVisual API
#   key_url - The sensitive key utilized to access the AirVisual API in key form
#   
#   AirVisual API Endpoint: http://api.airvisual.com/v2/countries?key={{YOUR_API_KEY}}
#   Description: Method formats the base_url with the key_url and then sends an HTTP Request to the GET Endpoint above. Method then parses the JSON data retrieved from the endpoint, checking if it was a success or failure first. If failure, method stores an error response as a string and then returns it. If not a failure, method parses the list of supported countries and formats them using the helper method above before returning the string.
def get_supported_countries(base_url, key_url):
    final_response = ""
    countries_url = base_url+"countries?"
    full_url = countries_url+key_url.lstrip("&")

    headers = {}
    payload = json.dumps({})
    raw_response = requests.get(full_url, headers=headers, data=payload)

    data = json.loads(raw_response.text)

    if not data["status"] == "success":
        final_response = "Error obtaining data! Location may not be supported, or there may be mispellings/typos in the prompt. Try '@AirVisualBot help' for further information!"
    else: 
        base_response = "List of Supported Countries: "
        country_dict = data["data"]

        country_list = extract_list_dict_values(country_dict)
        final_list = list_to_string(country_list)
        final_string = info_formatter(final_list, len(country_list))

        final_response = base_response+final_string
    return final_response

# get_supported_states() method to return the list of supported states in a supported country within the AirVisual API
#   base_url - The base URL address that is built upon for the AirVisual API
#   key_url - The sensitive key utilized to access the AirVisual API in key form
#   country - The country that the supported states are in
#
#   AirVisual API Endpoint: http://api.airvisual.com/v2/states?country={{COUNTRY_NAME}}&key={{YOUR_API_KEY}}
#   Description: Method formats the base_url with the country parameter and the key_url and then sends an HTTP Request to the GET Endpoint above. Method then parses the JSON data retrieved from the endpoint, checking if it was a success or failure first. If failure, method stores an error response as a string and then returns it. If not a failure, method parses the list of supported states in the country and formats them using the helper method above before returning the string.
def get_supported_states(base_url, key_url, country):
    final_response = ""

    states_url = base_url+"states?"
    full_url = states_url +"country=" + country + key_url

    headers = {}
    payload = json.dumps({})
    raw_response = requests.get(full_url, headers=headers, data=payload)

    data = json.loads(raw_response.text)

    if not data["status"] == "success":
        final_response = "Error obtaining data! Location may not be supported, or there may be mispellings/typos in the prompt. Try '@AirVisualBot help' for further information!"
    else:
        base_response = "List of Supported States in " + country.upper() + ": "

        state_dict = data["data"]

        state_list = extract_list_dict_values(state_dict)
        final_list = list_to_string(state_list)
        final_string = info_formatter(final_list, len(state_list))
        
        final_response = base_response + final_string
    return final_response

# get_supported_cities() method to return the list of supported cities in a supported state in a supported country within the AirVisual API
#   base_url - The base URL address that is built upon for the AirVisual API
#   key_url - The sensitive key utilized to access the AirVisual API in key form
#   state - The state that the supported countries are in
#   country - The country that the state is in
#
#   AirVisual API Endpoint: http://api.airvisual.com/v2/cities?state={{STATE_NAME}}&country={{COUNTRY_NAME}}&key={{YOUR_API_KEY}}
#   Description: Method formats the base_url with the state and country parameters, as well as the key_url and then sends an HTTP Request to the GET Endpoint above. Method then parses the JSON data retrieved from the endpoint, checking if it was a success or failure first. If failure, method stores an error response as a string and then returns it. If not a failure, method parses the list of supported cities in the state and in the country and formats them using the helper method above before returning the string.
def get_supported_cities(base_url, key_url, state, country):
    final_response = ""

    cities_url = base_url + "cities?"
    full_url = cities_url + "state=" + state + "&country=" + country + key_url

    headers = {}
    payload = json.dumps({})
    raw_response = requests.get(full_url, headers=headers, data=payload)

    data = json.loads(raw_response.text)

    if not data["status"] == "success":
        final_response = "Error obtaining data! Location may not be supported, or there may be mispellings/typos in the prompt. Try '@AirVisualBot help' for further information!"
    else:
        base_response = "List of Supported Cities in " + state.upper() + ", " + country.upper() + ": "

        city_dict = data["data"]

        city_list = extract_list_dict_values(city_dict)
        final_list = list_to_string(city_list)
        final_string = info_formatter(final_list, len(city_list))

        final_response = base_response + final_string
    return final_response

# current_weather_summary() method to return information about the current weather in a specified city.
#   city_dict - The dictionary of current weather obtained from the AirVisual API
#   city_name - The name of the city intended to retrieve weather information about
#   
#   Description: Method checks to make sure the "tp" (temperature), "pr" (air pressure), "hu" (humidity), "ws" (wind speed), and "wd" (wind direction) keys exist in the city_dict dictionary before parsing each one and adding it to the payload (city_response). If all are obtained, the method successfully retrieves temperature, air pressure, humidity, wind speed, and wind direction values from the AirVisual API response payload before successivelly formatting each one into a final string utilized to respond to the user query.
def current_weather_summary(city_dict, city_name):
    city_response = ""
    if "tp" in city_dict.keys():
        temp = city_dict["tp"]
        city_response += "Temperature - " + str(temp) + "\N{DEGREE SIGN}C\n"
    if "pr" in city_dict.keys():
        pressure = city_dict["pr"]
        city_response += "Air Pressure - " + str(pressure) + " hPa\n"
    if "hu" in city_dict.keys():
        humidity = city_dict["hu"]
        city_response += "Humidity - " + str(humidity) + "%\n"
    if "ws" in city_dict.keys():
        wind_speed = city_dict["ws"]
        city_response += "Wind - " + str(wind_speed) + " m/s"
    if "wd" in city_dict.keys():
        wind_dir = city_dict["wd"]
        card = get_cardinal_direction(wind_dir)
        city_response += " at angle of " + str(wind_dir) + "\N{DEGREE SIGN} (" + card + ")"

    return city_response

# current_pollution_summary() method to return information about the current pollution in a specified city.
#   city_dict - The dictionary of current weather obtained from the AirVisual API
#   city_name - The name of the city intended to retrieve pollution information about
#   
#   Description: Method first instantiates the final string as a variable, while also instantiating two dictionaries: 1) names of the pollutants as encoded by the AirVisual API creators, and 2) units of the pollutants in metrics that are outlined in the AirVisual API (unused dictionary ultimately). The method then checks to see if there is a pollutant that possesses a US Air Quality Rating of over 0 (non-zero). If not, the method returns a string stating that there is no pollutant above zero, meaning that the city has good air quality. If so, however, the method checks to see which pollutant is most present in the air of the city, then formats a string using the pollutants_names dictionary and generates a message personalized to the extent of that polluntant's air quality rating (higher is more hazardous).
def current_pollution_summary(city_dict, city_name):
    city_response = ""
    pollutant_names = {
        "p2": "Particulate Matter (diameter < 2.5 microns)",
        "p1": "Particulate Matter (diameter < 10 microns)", 
        "o3": "Ozone (O3)",
        "n2": "Nitrogen Dioxide (NO2)",
        "s2": "Sulfur Dioxide (SO2)",
        "co": "Carbon Monoxide (CO)"
    }
    pollutant_units = {
        "p2": "\u03BCg/m\u00B3",
        "p1": "\u03BCg/m\u00B3",
        "o3": "ppb",
        "n2": "ppb",
        "s2": "ppb",
        "co": "ppm"
    }
    if city_dict["aqius"] == 0:
        city_response += "Currently, no pollutant in " + city_name + " has a positive US Air Quality Index Rating." + new_line + "This is a strong indicator that " + city_name + " possesses non-hazardous air. Excellent job " + city_name + "!"
    else:
        city_response += "Main Pollutant - "
        main_poll = city_dict["mainus"]
        poll_name = pollutant_names[main_poll]
        city_response += poll_name + new_line

        aqi_poll = city_dict["aqius"]
        city_response += "The current US Air Quality Rating of " + poll_name + " in " + city_name + " is " + str(aqi_poll) + "." + new_line
        if aqi_poll < 50:
            city_response += "This is a generally a great air quality rating (" + str(aqi_poll) + "<50); " + city_name + " deserves recognition!"
        else :
            city_response += "This is air quality rating is not great (" + str(aqi_poll) + ">50)! The air of " + city_name + " is potentially hazardous, and its inhabitants and government agencies need to actively minimize emissions!"
    return city_response

# get_temp() method to return information about the temperature of a specified city, along with a personalized message relating to the magnitude of the temperature.
#   city_dict - The dictionary of current weather obtained from the AirVisual API
#   city_name - The name of the city intended to retrieve temperature information about
#
#   Description: Method first checks to see if temperature exists in the city_dict dictionary. If it doesn't, returns a message stating so. If it does contain a valid temperature, it parses the temperature and appends the given temperature to the string in a nice format. Then, based on the magnitude of the temperature, it generates a personalized message that is also appended to the string. Finally, it returns the string.
def get_temp(city_dict, city_name):
    city_response = ""
    if "tp" in city_dict.keys():
        current_temp = city_dict["tp"]
        city_response += "The current temperature in " + city_name + " is " + str(current_temp) + "\N{DEGREE SIGN}C." + new_line
        if current_temp < 0:
            city_response += "Brrrrrrrrr, this is below freezing!! If you are in " + city_name + ", you would probably want to wear a parka!"
        elif current_temp < 10:
            city_response += "This is pretty cold! If you plan on being in " + city_name + " today, you should probably grab a jacket!"
        elif current_temp < 20:
            city_response += "This is pretty average weather. A long-sleeve T-shirt and full pants would be fine in " + city_name + " today!"
        elif current_temp < 35:
            city_response += "This is nice weather! If you are in " + city_name + ", tank tops and shorts would be perfect to wear!"
        else:
            city_response += "It is way too hot in " + city_name + " right now!! Stay inside and make sure the AC Unit is turned on!"
    else:
        city_response += "No temperature data found in the system for " + city_name + ". DM me 'help' for more information!"
    return city_response

# get_pressure() method to return information about the air pressure (in hPa) of a specified city, along with a personalized message relating to the magnitude of the air pressure.
#   city_dict - The dictionary of current weather obtained from the AirVisual API
#   city_name - The name of the city intended to retrieve air pressure information about
#
#   Description: Method first checks to see if air pressure exists in the city_dict dictionary. If it doesn't, returns a message stating so. If it does contain a valid air pressure, it parses the pressure and appends the given pressure to the string in a nice format. Then, based on the magnitude of the pressure, it generates a personalized message that is also appended to the string. Finally, it returns the string.
def get_pressure(city_dict, city_name):
    city_response = ""
    if "pr" in city_dict.keys():
        current_pressure = city_dict["pr"]
        city_response += "The current air pressure in " + city_name + " is " + str(current_pressure) + " hPa." + new_line
        if current_pressure < 1007:
            city_response += "If you are prone to migraines, I would avoid the low air pressure of " + city_name + "!"
        elif current_pressure < 1020:
            city_response += "The pressure in " + city_name + " seems to be pretty normal!"
        else:
            city_response += "This relatively low pressure in " + city_name + " may make you susceptible to decompression sickness!"
    else:
        city_response += "No air pressure data found in the system for " + city_name + ". DM me 'help' for more information!"
    return city_response

# get_humidity() method to return information about the humidity (%) of a specified city, along with a personalized message relating to the magnitude of the humidity.
#   city_dict - The dictionary of current weather obtained from the AirVisual API
#   city_name - The name of the city intended to retrieve humidity information about
#
#   Description: Method first checks to see if humidity exists in the city_dict dictionary. If it doesn't, returns a message stating so. If it does contain a valid humidity, it parses the humidity and appends the given humidity to the string in a nice format. Then, based on the magnitude of the humidity, it generates a personalized message that is also appended to the string. Finally, it returns the string.
def get_humidity(city_dict, city_name):
    city_response = ""
    if "hu" in city_dict.keys():
        current_humidity = city_dict["hu"]
        city_response += "The current humidity in " + city_name + " is " + str(current_humidity) + "%." + new_line
        if current_humidity < 25:
            city_response += "This is relatively non-humid. Enjoy the clear and crisp weather" + city_name + ", but watch out for possible rain!"
        elif current_humidity < 75:
            city_response += "This is relatively humid. It might have rained recently in " + city_name + ", so be careful on the roads!"
        else:
            city_response += "This is EXTREMELY humid! Beware of stuffy weather in " + city_name + " today. Drink lots of water!"
    else: 
        city_response += "No humidity data found in the system for " + city_name + ". DM me 'help' for more information!"
    return city_response

# get_wind() method to return information about the wind (both speed , in m/s, and direction, in degrees) of a specified city, along with a personalized message relating to the magnitude of the wind and direction of it.
#   city_dict - The dictionary of current weather obtained from the AirVisual API
#   city_name - The name of the city intended to retrieve wind information about
#
#   Description: Method first checks to see if wind speed and wind direction exist in the city_dict dictionary. If they don't, returns a message stating so. If they do exist, it parses the wind speed and direction and appends them to the string, in addition to the cardinal direction the magnitude of degrees corresponds to, in a nice format. Then, based on the magnitude of the wind speed and its direction, method generates a personalized message that is also appended to the string. Finally, it returns the string.
def get_wind(city_dict, city_name):
    city_response = ""
    if "ws" and "wd" in city_dict.keys():
        current_wspeed = city_dict["ws"]
        current_wdir = city_dict["wd"]
        card = get_cardinal_direction(current_wdir)
        city_response += "The wind speed in " + city_name + " is currently " + str(current_wspeed) + " m/s at an angle of " + str(current_wdir) + "\N{DEGREE SIGN} (" + card + ")." + new_line
        if current_wspeed > 10:
            opp_wdir = (current_wdir + 180) % 360
            opp_card = get_cardinal_direction(opp_wdir)
            city_response += "This is extremly windy! I would be sure to bring a jacket and face " + opp_card + " when walking in " + city_name + "!"
        elif current_wspeed > 0:
            city_response += "Not too windy in " + city_name + " today! Enjoy your day!"
        else:
            city_response += "Enjoy your wind-free day in " + city_name + " today!"
    return city_response

# get_summary_lat_long() method to retrive weather, pollution, temperature, humidity, air pressure, or wind information regarding a certain GPS coordination (latitude and longitude). Note that the AirVisual API limits longitude to [-180, 180] and latitude to [-90, 90].
#   base_url - The base URL address that is built upon for the AirVisual API
#   key_url - The sensitive key utilized to access the AirVisual API in key form
#   lat - The latitude coordinates specified by the user
#   long - The longitude coordinates specified by the user
#   weather_bool - Integer value utilized to represent whether the user is asking for a weather summary (0), pollution summary (1), or specifics regarding the weather (2) for the coordinates
#   temp_item - Default value utilized to represent whether user is querying for temperature (0), air pressure (1), humidity (2), or wind information (3) for the city for the coordinates
#
#   API Endpoint: http://api.airvisual.com/v2/nearest_city?lat={{LATITUDE}}&lon={{LONGITUDE}}&key={{YOUR_API_KEY}}
#   Description: Method first instantiates a response variable prior to forming the HTTP Endpoint URL as specified above with the base_url, key_url, lat, and long parameters. From there, the requests library is utilized to perform an HTTP request and retrieve JSON data. If the JSON data signifies a failed request, the response variable is reassigned as such to inform the user of this. If the JSON data signifies a successful request, it then uses the other two parameters (weather_bool and temp_item) to leverage the according helper method defined above. In all cases, it creates a base_response variable to specify the nearest city that was geolocated using the latitude and longitude GPS coordinates entered by the user, as this is the city whose information will be retrieved upon in the AirVisual API. Finally, from the execution of the aforementioned helper methods, it appends the specific information regarding this request to the string, prior to returning it.
def get_summary_lat_long(base_url, key_url, lat, long, weather_bool=0, temp_item=0):
    final_response = ""
    coord_url = base_url + "nearest_city?"
    full_url = coord_url + "lat=" + lat + "&lon=" + long + key_url

    headers = {}
    payload = json.dumps({})
    raw_response = requests.get(full_url, headers=headers, data=payload)
    data = json.loads(raw_response.text)
    
    city_dict = data["data"]
    if not data["status"] == "success":
        final_response = "Error obtaining data! Location may not be supported, or there may be mispellings/typos in the prompt. Try '@AirVisualBot help' for further information!"
    else:
        base_response = "Nearest City: " + city_dict["city"] + ", " + city_dict["state"] + ", " + city_dict["country"] + new_line

        final_string = ""
        if weather_bool == 0: 
            final_string = current_weather_summary(city_dict["current"]["weather"], city_dict["city"])
        elif weather_bool == 1:
            final_string = current_pollution_summary(city_dict["current"]["pollution"], city_dict["city"])
        else:
            if temp_item == 0:
                final_string = get_temp(city_dict["current"]["weather"], city_dict["city"])
            elif temp_item == 1:
                final_string = get_pressure(city_dict["current"]["weather"], city_dict["city"])
            elif temp_item == 2:
                final_string = get_humidity(city_dict["current"]["weather"], city_dict["city"])
            else :
                final_string = get_wind(city_dict["current"]["weather"], city_dict["city"])

        final_response = base_response + final_string
    return final_response

# get_summary_specified_city() method to retrive weather, pollution, temperature, humidity, air pressure, or wind information regarding a city supported by the AirVisual API.
#   base_url - The base URL address that is built upon for the AirVisual API
#   key_url - The sensitive key utilized to access the AirVisual API in key form
#   city - The city specified by the user to retrieve information about
#   state - The state specified by the user to retrieve information about
#   country - The country specified by the user to retrieve information about
#   weather_bool - Integer value utilized to represent whether the user is asking for a weather summary (0), pollution summary (1), or specifics regarding the weather (2) for the coordinates
#   temp_item - Default value utilized to represent whether user is querying for temperature (0), air pressure (1), humidity (2), or wind information (3) for the city for the coordinates
#
#   API Endpoint: http://api.airvisual.com/v2/city?city={{CITY}}&state={{STATE}}&country={{COUNTRY}}&key={{YOUR_API_KEY}}
#   Description: Method first instantiates a response variable prior to forming the HTTP Endpoint URL as specified above with the base_url, key_url, city, state, and country parameters. From there, the requests library is utilized to perform an HTTP request and retrieve JSON data. If the JSON data signifies a failed request, the response variable is reassigned as such to inform the user of this. If the JSON data signifies a successful request, it then uses the other two parameters (weather_bool and temp_item) to leverage the according helper method defined above. In all cases, it creates a base_response variable to specify the city whose information was retrieved upon in the AirVisual API. Finally, from the execution of the aforementioned helper methods, it appends the specific information regarding this request to the string, prior to returning it.
def get_summary_specified_city(base_url, key_url, city, state, country, weather_bool=0, temp_item=0):
    final_response = ""

    specified_url = base_url + "city?"
    full_url = specified_url + "city=" + city + "&state=" + state + "&country=" + country + key_url

    headers = {}
    payload = json.dumps({})
    raw_response = requests.get(full_url, headers=headers, data=payload)
    data = json.loads(raw_response.text)

    if not data["status"] == "success":
        final_response = "Error obtaining data! Location may not be supported, or there may be mispellings/typos in the prompt. Try '@AirVisualBot help' for further information!"
    else:
        city_dict = data["data"]

        base_response = "Location: " + city_dict["city"] + ", " + city_dict["state"] + ", " + city_dict["country"] + new_line

        final_string = ""
        if weather_bool == 0:
            final_string = current_weather_summary(city_dict["current"]["weather"], city_dict["city"])
        elif weather_bool == 1:
            final_string = current_pollution_summary(city_dict["current"]["pollution"], city_dict["city"])
        else:
            if temp_item == 0:
                final_string = get_temp(city_dict["current"]["weather"], city_dict["city"])
            elif temp_item == 1:
                final_string = get_pressure(city_dict["current"]["weather"], city_dict["city"])
            elif temp_item == 2:
                final_string = get_humidity(city_dict["current"]["weather"], city_dict["city"])
            else :
                final_string = get_wind(city_dict["current"]["weather"], city_dict["city"])

        final_response = base_response + final_string
    return final_response
# get_help_response() method.
#   Description: Method simply returns an informative message with further instructions to read 'ReadMe.md' file in GitHub in case user requires help!
def get_help_response():
    final_response = "Hi I'm AirVisualBot! I'm here to respond to queries about weather and air quality in various places of the world.\n\nFor a list of my responsive commands, check out this link: https://github.com/kss7yy/Sarnaik_Kunaal_DS3002_DataProject2"
    return final_response

# check_mentions() method to check the mentions of my Twitter account when called. Goes through each tweet using the Tweepy.Cursor() class, making sure to update the id of the tweet so that only non-duplicates are checked. From there, parses the text of the tweet in order to perform the according request for the AirVisual API library. After determining the response using one of the methods above, formats the response into a text that can be sent from my Twitter account, also using Tweepy. Please see inline comments for further information!
#   api - Tweepy API instance that is utilized to read and write information from my Twitter account
#   since_id - The latest id of the tweet that was most recently addressed. Updated everytime this method is run in order to ensure tweets are not read/addessed more than once!
#
#   Description: See inline comment.s
def check_mentions(api, since_id):
    # Logs the retrieval of mentions to signify to console that this method is being performed.
    logger.info("Retrieving mentions")

    # Default new_since_id, in case only one tweet exists in this iteration.
    new_since_id = since_id

    #Iterates through the tweets in the Cursor item, using the since_id to ensure that only non-duplicates are addressed.
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():

        #Updates new_since_id if the current tweet's id is later than the previous.
        new_since_id = max(tweet.id, new_since_id)

        #Makes sure tweet has not already been replied to by the Twitter account.
        if tweet.in_reply_to_status_id is not None:
            continue
        
        # Obtains the sensitive AirVisual API Key from the environment and formats it into a URL
        key = os.getenv("AIRVISUAL_KEY")
        key_url = "&key=" + key

        # Creates the base URL of the AirVisual API utilized to perform HTTP Requests.
        base = "http://api.airvisual.com/v2/"
        response = ""

        # Retrieves the query from the current tweet and lowercases all characters to ensure no spelling identities are incorrectly performed later on.
        prompt = tweet.text.lower()
        
        # If statement that loops through each condition that matches an according retrieval request. Herein lies the functionality and usability of the application.

        if "help" in prompt:
            #FUNCTION 1: Help message. Retrieves introductory information and stores it in response for user help requests on the application.
            response = get_help_response()
        elif "list supported countries" in prompt:
            #FUNCTION 2: Supported Countries. Retrieves all the countries supported by the AirVisual API
            response = get_supported_countries(base, key_url)
        elif "list supported states in" in prompt:
            #FUNCTION 3: Supported States. Retrieves all the States supported by the AirVisual API. User must specify a country in the supported format, which is parsed below!
            country = prompt[prompt.index("in")+3:]
            response = get_supported_states(base, key_url, country)
        elif "list supported cities in" in prompt:
            #FUNCTION 4: Supported Cities. Retrieves all the Cities supported by the AirVisual API. User must specify a state and a country in the supported format, which are both parsed below!
            state = prompt[prompt.index("in")+3:prompt.index(",")]
            country = prompt[prompt.index(",")+2:]
            response = get_supported_cities(base, key_url, state, country)
        elif "weather summary of lat" in prompt:
            # FUNCTION 5: Weather Summary (GPS Coordinates). Retrieves summary of weather information regarding nearest city specified by the GPS coordinates, which are both parsed below! 
            lat = prompt[prompt.index("lat") + 4: prompt.index("and long")-1]
            long = prompt[prompt.index("long") + 5:]
            response = get_summary_lat_long(base, key_url, lat, long, 0)
        elif "pollution summary of lat" in prompt:
            # FUNCTION 6: Pollution Summary (GPS Coordinates). Retrieves summary of pollution information regarding nearest city specified by the GPS coordinates, which are both parsed below! 
            lat = prompt[prompt.index("lat") + 4: prompt.index("and long")-1]
            long = prompt[prompt.index("long") + 5:]
            response = get_summary_lat_long(base, key_url, lat, long, 1)
        elif "weather summary of" in prompt:
            # FUNCTION 7: Weather Summary (Supported city, state, and country format). Retrieves summary of weather information regarding city specified by the supported city, state, and country the user enters, which are all parsed below! 
            city = prompt[prompt.index("of")+3: prompt.index(",")]
            state = prompt[prompt.index(",")+2: prompt.index("in country")-1]
            country = prompt[prompt.index("in country")+11:]
            response = get_summary_specified_city(base, key_url, city, state, country, 0)
        elif "pollution summary of" in prompt:
            # FUNCTION 8: Pollution Summary (Supported city, state, and country format). Retrieves summary of pollution information regarding city specified by the supported city, state, and country the user enters, which are all parsed below! 
            city = prompt[prompt.index("of")+3: prompt.index(",")]
            state = prompt[prompt.index(",")+2: prompt.index("in country")-1]
            country = prompt[prompt.index("in country")+11:]
            response = get_summary_specified_city(base, key_url, city, state, country, 1)
        elif "temperature of lat" in prompt:
            # FUNCTION 9: Current Temperature (GPS Coordinates). Retrieves current temperature information regarding nearest city specified by the GPS coordinates, which are both parsed below! 
            lat = prompt[prompt.index("lat") + 4: prompt.index("and long")-1]
            long = prompt[prompt.index("long") + 5:]
            response = get_summary_lat_long(base, key_url, lat, long, 2, 0)
        elif "temperature of" in prompt:
            # FUNCTION 10: Current Temperature (supported city, state, and country format). Retrieves current temperature information regarding supported city, state, and country specified by user; they are all parsed below.
            city = prompt[prompt.index("of")+3: prompt.index(",")]
            state = prompt[prompt.index(",")+2: prompt.index("in country")-1]
            country = prompt[prompt.index("in country")+11:]
            response = get_summary_specified_city(base, key_url, city, state, country, 2, 0)
        elif "pressure of lat" in prompt:
            # FUNCTION 11: Current Air Pressure (GPS Coordinates). Retrieves current air pressure information regarding nearest city specified by the GPS coordinates, which are both parsed below! 
            lat = prompt[prompt.index("lat") + 4: prompt.index("and long")-1]
            long = prompt[prompt.index("long") + 5:]
            response = get_summary_lat_long(base, key_url, lat, long, 2, 1)
        elif "pressure of" in prompt:
            # FUNCTION 12: Current Air Pressure (supported city, state, and country format). Retrieves current air pressure information regarding supported city, state, and country specified by user; they are all parsed below.
            city = prompt[prompt.index("of")+3: prompt.index(",")]
            state = prompt[prompt.index(",")+2: prompt.index("in country")-1]
            country = prompt[prompt.index("in country")+11:]
            response = get_summary_specified_city(base, key_url, city, state, country, 2, 1)
        elif "humidity of lat" in prompt:
            # FUNCTION 13: Current Humidity (GPS Coordinates). Retrieves current humidity information regarding nearest city specified by the GPS coordinates, which are both parsed below! 
            lat = prompt[prompt.index("lat") + 4: prompt.index("and long")-1]
            long = prompt[prompt.index("long") + 5:]
            response = get_summary_lat_long(base, key_url, lat, long, 2, 2)
        elif "humidity of" in prompt:
            # FUNCTION 14: Current Humidity (supported city, state, and country format). Retrieves current humidity information regarding supported city, state, and country specified by user; they are all parsed below.
            city = prompt[prompt.index("of")+3: prompt.index(",")]
            state = prompt[prompt.index(",")+2: prompt.index("in country")-1]
            country = prompt[prompt.index("in country")+11:]
            response = get_summary_specified_city(base, key_url, city, state, country, 2, 2)
        elif "wind information of lat" in prompt:
            # FUNCTION 15: Current Wind Information (GPS Coordinates). Retrieves current wind information (speed and direction) regarding nearest city specified by the GPS coordinates, which are both parsed below! 
            lat = prompt[prompt.index("lat") + 4: prompt.index("and long")-1]
            long = prompt[prompt.index("long") + 5:]
            response = get_summary_lat_long(base, key_url, lat, long, 2, 3)
        elif "wind information of" in prompt:
            # FUNCTION 16: Current Wind Information (supported city, state, and country format). Retrieves current wind information regarding supported city, state, and country specified by user; they are all parsed below.
            city = prompt[prompt.index("of")+3: prompt.index(",")]
            state = prompt[prompt.index(",")+2: prompt.index("in country")-1]
            country = prompt[prompt.index("in country")+11:]
            response = get_summary_specified_city(base, key_url, city, state, country, 2, 3)
        else:
            # CATCH-ALL Command --> Informs the user that a supported command wasn't given via the tweet, and prompts them to try the help query.
            response = "Please give me a proper command! Try '@AirVisualBot help' for further information!"

        # Logs to the console that we are responding to the user with the response specified from the above conditional statement.
        logger.info(f"Responding to {tweet.user.name} with {response}")

        # Prepends the tag of the user (screen_name) to the response so that it comes in as a reply.
        final_response = "@" + tweet.user.screen_name + " " + response

        # Follows the user if they are not followed by the account already.
        if not tweet.user.following:
            tweet.user.follow()
        
        # Checks to see if the length of the response is more than 280 characters (Twitter's tweet character limit). If it is, sends the response via direct message. If it is within Twitter's character limit, replies to the user's tweet!
        if len(response) <= 280:
            api.update_status(
                status=final_response,
                in_reply_to_status_id=tweet.id
            )
        else:
            # Informs user via reply tweet that they are going to be direct messaged due to character limit.
            api.update_status(
                status="@" + tweet.user.screen_name + " Response contains too many characters for tweet. Check your direct messages!",
                in_reply_to_status_id=tweet.id
            )
            # Try-catch statement to send direct message to the user with the response, catching exception of being unable to do so (functionality doesn't work, however), and trace is still printed and execution of program is stopped.
            try:
                api.send_direct_message(tweet.user.id, final_response)
            except tweepy.error.TweepError as e:
                logger.error("Error! Cannot send direct message to this user!", exc_info=True)
                api.update_status(
                    status="@" + tweet.user.screen_name + " We could not respond to your query via direct message! You must enable direct messages to be accepted in order for this to happen!"
                )
                pass
    return new_since_id

# Informal Main method: Creates API instance of Twitter account, instantiates since_mention_id variable to keep track of latest Tweet that was responded to, and goes through an infinite loop of checking mentions and addressing them, intermittently sleeping for 60 seconds (1 minute)
def main():
    api = create_api()
    since_mention_id = 1
    while True:
        since_mention_id = check_mentions(api, since_mention_id)
        logger.info("Waiting...")
        time.sleep(60)

# Actual Main Method that Python recognizes.
if __name__ == "__main__":
    main()