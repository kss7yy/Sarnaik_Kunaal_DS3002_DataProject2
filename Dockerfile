# Builds the Docker Container from the base python:3.7-alpine container.
FROM python:3.7-alpine

# Copies over the bots/config.py and bots/sarnaik_bot.py from the host machine to the Docker Container when built.
#   bots/config.py - Python script to set up authentication and configuration to the Twitter account via developer credentials.
#   bots/sarnaik.py - Python script containing the executable information necessary for the Twitter application to successfully run
COPY bots/config.py /bots/
COPY bots/sarnaik_bot.py /bots/

# Copies over the requirements.txt file frozen by pip to a /tmp directory in the Docker Container.
#   requirement.txt - Contains the necessary requirements (Python libraries and modules) to run the Twitter application Python script.
COPY requirements.txt /tmp

# Installs the python libraries and modules necessary for the Twitter application to be successfully executed using pip3 (Python's installer)
RUN pip3 install -r /tmp/requirements.txt

# Changes the working directory for the command to be executed in the Docker Container when it is run.
WORKDIR /bots

# Default command that is utilized when the Docker container is run.
CMD ["python3", "sarnaik_bot.py"]

# Reminder for reader, proper usability of the application is as follows if running locally:
#   "docker run -it -e CONSUMER_KEY="uDRNy31oWfoiKV9AvPoNavy0I" -e CONSUMER_SECRET="lnAL5VAgZLWNspQVpd3X6tEo47PRCmsPEwuxpvLCLSR08DMa4O" -e ACCESS_TOKEN="622518593-j7gWSqzQO31ju7Bf7idB47NlZeSENsuADGU9B69I" -e ACCESS_TOKEN_SECRET="iutFsxvP5IglRckJ1I1why6017xMNkzxqBID48Azw0GvT" kss7yy/sarnaik_airvisual_API_twitter_bot"