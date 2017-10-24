# Motion Detector Project

This code runs on RaspberryPi 3 and is used to check our Ping Pong table room in my company's offices to see if it's available or not :)
It uses a PIR motion detection sensor to detect movement and updates the Mysql DB accordingly.
In addition, a Slack bot queries the DB to determine if there's an ongoing open session.

# Pre-Requisites

* Raspberry Pi
* PIR motion detector
* Raspbian Jessie

# Getting Started

1. Run the setup script `./setup.sh`

2. Edit the `config.properties` file if you changed your mysql db user and password

3. Run `python motion_detector.py` to begin monitoring

4. Edit `pingpongbot.py` and replace `SLACK_BOT_TOKEN` and `SLACK_BOT_NAME` with the relevant Slack information

5. Run `python pingpongbot.py` to start the Slack bot
