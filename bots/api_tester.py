#!/usr/bin/env python3
'''
Name: Kunaal Sarnaik (kss7yy@virginia.edu)
Course: DS 3002 - Data Science Systems (Spring 2021)
Date: May 10th, 2021
Professor: Neal Magee, Ph.D.
Project Name: Air Visual API Twitter Bot
Assignment: DS3002 Data Project #2

File Name: api_tester.py
File Purpose: Used for local testing with console.
'''
import requests
import json
import os

new_line = "\n\n"

def info_formatter(s, length):
    s = s.rstrip(',')
    s = s.lstrip()
    if length > 1:
        last_comma = s.rindex(',', 0, len(s))
        s = s[:last_comma] + " and" + s[last_comma+1:]
    return s

def extract_list_dict_values(d):
    values = []
    for ele in d:
        for key in ele.keys() :
            values.append(ele[key])
    return values

def list_to_string(l):
    s = ""
    for item in l:
        s += " " + item + ","
    return s

def get_cardinal_direction(deg):
    #wind direction, as an angle of 360° (N=0, E=90, S=180, W=270)
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

def get_supported_countries(base_url, key_url):
    countries_url = base_url+"countries?"
    full_url = countries_url+key_url.lstrip("&")

    headers = {}
    payload = json.dumps({})
    raw_response = requests.get(full_url, headers=headers, data=payload)

    data = json.loads(raw_response.text)

    base_response = "List of Supported Countries: "

    country_dict = data["data"]

    country_list = extract_list_dict_values(country_dict)
    final_list = list_to_string(country_list)
    final_string = info_formatter(final_list, len(country_list))

    final_response = base_response+final_string
    return final_response

def get_supported_states(base_url, key_url, country):
    states_url = base_url+"states?"
    full_url = states_url +"country=" + country + key_url

    headers = {}
    payload = json.dumps({})
    raw_response = requests.get(full_url, headers=headers, data=payload)

    data = json.loads(raw_response.text)

    base_response = "List of Supported States in " + country.upper() + ": "

    state_dict = data["data"]

    state_list = extract_list_dict_values(state_dict)
    final_list = list_to_string(state_list)
    final_string = info_formatter(final_list, len(state_list))
    
    final_response = base_response + final_string

    return final_response

def get_supported_cities(base_url, key_url, state, country):
    cities_url = base_url + "cities?"
    full_url = cities_url + "state=" + state + "&country=" + country + key_url

    headers = {}
    payload = json.dumps({})
    raw_response = requests.get(full_url, headers=headers, data=payload)

    data = json.loads(raw_response.text)

    base_response = "List of Supported Cities in " + state.upper() + ", " + country.upper() + ": "

    city_dict = data["data"]

    city_list = extract_list_dict_values(city_dict)
    final_list = list_to_string(city_list)
    final_string = info_formatter(final_list, len(city_list))

    final_response = base_response + final_string

    return final_response

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
            city_response += "This is pretty average weather. A long-sleeve T-shirt and full pants would be fine in " + city_name + "today!"
        elif current_temp < 35:
            city_response += "This is nice weather! If you are in " + city_name + ", tank tops and shorts would be perfect to wear!"
        else:
            city_response += "It is way too hot in " + city_name + "right now!! Stay inside and make sure the AC Unit is turned on!"
    else:
        city_response += "No temperature data found in the system for " + city_name + ". DM me 'help' for more information!"
    return city_response

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

def get_wind(city_dict, city_name):
    city_response = ""
    if "ws" and "wd" in city_dict.keys():
        current_wspeed = city_dict["ws"]
        current_wdir = city_dict["wd"]
        card = get_cardinal_direction(current_wdir)
        city_response += "The wind speed in " + city_name + " is currently " + current_wspeed + " m/s at an angle of " + current_wdir + "\N{DEGREE SIGN} (" + card + ")." + new_line
        if current_wspeed > 10:
            opp_wdir = (current_wdir + 180) % 360
            opp_card = get_cardinal_direction(opp_wdir)
            city_response += "This is extremly windy! I would be sure to bring a jacket and face " + opp_card + " when walking in " + city_name + "!"
        elif current_wspeed > 0:
            city_response += "Not too windy in " + city_name + " today! Enjoy your day!"
        else:
            city_response += "Enjoy your wind-free day in " + city_name + " today!"
    return city_response

def get_summary_lat_long(base_url, key_url, lat, long, weather_bool=0, temp_item=0):
    coord_url = base_url + "nearest_city?"
    full_url = coord_url + "lat=" + lat + "&lon=" + long + key_url

    headers = {}
    payload = json.dumps({})
    raw_response = requests.get(full_url, headers=headers, data=payload)
    data = json.loads(raw_response.text)
    
    city_dict = data["data"]

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

def get_summary_specified_city(base_url, key_url, city, state, country, weather_bool=0, temp_item=0):
    specified_url = base_url + "city?"
    full_url = specified_url + "city=" + city + "&state=" + state + "&country=" + country + key_url

    headers = {}
    payload = json.dumps({})
    raw_response = requests.get(full_url, headers=headers, data=payload)
    data = json.loads(raw_response.text)

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

def main():
    key = os.getenv("AIRVISUAL_KEY")
    key_url = "&key=" + key
    base = "http://api.airvisual.com/v2/"
    response = ""
    
    prompt = input('Prompt: ')
    prompt = prompt.lower()

    if prompt == "list supported countries":
        response = get_supported_countries(base, key_url)

    elif "list supported states in" in prompt:
        country = prompt[prompt.index("in")+3:]
        response = get_supported_states(base, key_url, country)

    elif "list supported cities in" in prompt:
        state = prompt[prompt.index("in")+3:prompt.index(",")]
        country = prompt[prompt.index(",")+2:]
        response = get_supported_cities(base, key_url, state, country)

    elif "weather summary of lat" in prompt:
        lat = prompt[prompt.index("lat") + 4: prompt.index("and long")-1]
        long = prompt[prompt.index("long") + 5:]
        response = get_summary_lat_long(base, key_url, lat, long, 0)

    elif "pollution summary of lat" in prompt:
        lat = prompt[prompt.index("lat") + 4: prompt.index("and long")-1]
        long = prompt[prompt.index("long") + 5:]
        response = get_summary_lat_long(base, key_url, lat, long, 1)

    elif "weather summary of" in prompt:
        city = prompt[prompt.index("of")+3: prompt.index(",")]
        state = prompt[prompt.index(",")+2: prompt.index("in country")-1]
        country = prompt[prompt.index("in country")+11:]
        response = get_summary_specified_city(base, key_url, city, state, country, 0)

    elif "pollution summary of" in prompt:
        city = prompt[prompt.index("of")+3: prompt.index(",")]
        state = prompt[prompt.index(",")+2: prompt.index("in country")-1]
        country = prompt[prompt.index("in country")+11:]
        response = get_summary_specified_city(base, key_url, city, state, country, 1)

    elif "temp of lat" in prompt:
        lat = prompt[prompt.index("lat") + 4: prompt.index("and long")-1]
        long = prompt[prompt.index("long") + 5:]
        response = get_summary_lat_long(base, key_url, lat, long, 2, 0)

    elif "temp of" in prompt:
        city = prompt[prompt.index("of")+3: prompt.index(",")]
        state = prompt[prompt.index(",")+2: prompt.index("in country")-1]
        country = prompt[prompt.index("in country")+11:]
        response = get_summary_specified_city(base, key_url, city, state, country, 2, 0)

    elif "pressure of lat" in prompt:
        lat = prompt[prompt.index("lat") + 4: prompt.index("and long")-1]
        long = prompt[prompt.index("long") + 5:]
        response = get_summary_lat_long(base, key_url, lat, long, 2, 1)

    elif "pressure of" in prompt:
        city = prompt[prompt.index("of")+3: prompt.index(",")]
        state = prompt[prompt.index(",")+2: prompt.index("in country")-1]
        country = prompt[prompt.index("in country")+11:]
        response = get_summary_specified_city(base, key_url, city, state, country, 2, 1)

    elif "humidity of lat" in prompt:
        lat = prompt[prompt.index("lat") + 4: prompt.index("and long")-1]
        long = prompt[prompt.index("long") + 5:]
        response = get_summary_lat_long(base, key_url, lat, long, 2, 2)

    elif "humidity of" in prompt:
        city = prompt[prompt.index("of")+3: prompt.index(",")]
        state = prompt[prompt.index(",")+2: prompt.index("in country")-1]
        country = prompt[prompt.index("in country")+11:]
        response = get_summary_specified_city(base, key_url, city, state, country, 2, 2)

    elif "wind information of lat" in prompt:
        lat = prompt[prompt.index("lat") + 4: prompt.index("and long")-1]
        long = prompt[prompt.index("long") + 5:]
        response = get_summary_lat_long(base, key_url, lat, long, 2, 3)

    elif "wind information of" in prompt:
        city = prompt[prompt.index("of")+3: prompt.index(",")]
        state = prompt[prompt.index(",")+2: prompt.index("in country")-1]
        country = prompt[prompt.index("in country")+11:]
        response = get_summary_specified_city(base, key_url, city, state, country, 2, 3)

    else:
        response = "Please give me a command!"
    print(response)

if __name__ == "__main__":
    main()