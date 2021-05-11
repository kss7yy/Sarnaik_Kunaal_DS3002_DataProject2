# tweepy-bots/bots/config.py
'''
Name: Kunaal Sarnaik (kss7yy@virginia.edu)
Course: DS 3002 - Data Science Systems (Spring 2021)
Date: May 10th, 2021
Professor: Neal Magee, Ph.D.
Project Name: Air Visual API Twitter Bot
Assignment: DS3002 Data Project #2

File Name: config.py
File Purpose: Utilized to authenticate credentials (passed in as environment variables) to the Twitter Developer API for my Twitter Account
'''
# Python modules and libraries needed for full functionality of this executable
import tweepy   # Python library for accessing Twitter's developer API
import logging  # Standard python module to emit log messages from this executable
import os       # Standard python module for accessing environment variables in the operating system

# Uses the logging Python module to inform errors and information messages that can help debug issues when they arise. Logs to console with time.
logger = logging.getLogger()

# create_api() method.
#   Description: Method first extracts the relevant keys from the environment utilized to authenticate credentials to the Twitter Developer Account and then access the Twitter API. Method then instantiates an api instance utilized to read/write information from the account using the keys and access tokens. Method then attempts to verify credentials to the API, and if it doesn't, catches an exception prompting the restart of the executable. Finally, logs to the console that the API was created and returns the api. This method is called in the bots/sarnaik_bot.py executable in order to ensure its full functionality.
def create_api():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api