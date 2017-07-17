# Motion Detector Project

This code runs on RaspberryPi 3 and is used to check our Ping Pong table room in my company's offices to see if it's available or not :)
It uses a PIR motion detection sensor to detect movement and updates the Mysql DB accordingly.
In addition, a Slack bot queries the DB to determine if there's an ongoing open session.

# Pre-Requisites

* RaspberryPi 3
* PIR motion detector
* Raspbian Jessie
* Python 2.7
* Pip
* Mysql server
* Slack client
* Slack bot integration token
* MysqlClient for Python

# Getting Started

1. Create a `config.properties` file in the root folder in the following format - 

```
[DatabaseSection]
database.host=<host>
database.user=<user>
database.password=<password>
```

2. Run `python motion_detector.py` to begin monitoring

3. Edit `pingpongbot.py` and replace `SLACK_BOT_TOKEN` and `SLACK_BOT_NAME` with the relevant Slack information

4. Run `python pingpongbot.py` to start the Slack bot
