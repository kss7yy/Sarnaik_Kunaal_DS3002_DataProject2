# tweepy-bots/bots/config.py
'''
Name: Kunaal Sarnaik (kss7yy@virginia.edu)
Course: DS 3002 - Data Science Systems (Spring 2021)
Date: May 10th, 2021
Professor: Neal Magee, Ph.D.
Project Name: Air Visual API Twitter Bot
Assignment: DS3002 Data Project #2

File Name: config.py
'''

import tweepy
import logging
import os

logger = logging.getLogger()

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