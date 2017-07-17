# Motion Detector Project

This code runs on RaspberryPi 3 and is used to check our Ping Pong table room in my company's offices to see if it's available or not :)
It uses a PIR motion detection sensor to detect movement and updates the Mysql DB accordingly.
It currently only provides a REST API endpoint to query the status but later on we will add a Slack bot user as well.

# Pre-Requisites

* RaspberryPi 3
* PIR motion detector
* Raspbian Jessie
* Python 2.7
* Pip
* Mysql Server
* Django
* MysqlClient for Python

# Getting Started

1. Create a `config.properties` file in the root folder in the following format - 

```
[DatabaseSection]
database.host=<host>
database.user=<user>
database.password=<password>
```

2. Configure the IP address of the RaspberryPi in the `/mysite/mysite/settings.py` file under `ALLOWED_HOSTS`

3. Start the server by running `python /mysite/manage.py runserver 0.0.0.0:8080`

4. Run `python motion_detector.py` to begin monitoring

5. Access the URL `<Raspberry Pi IP Address>:8080/myapp` to check the status of the sensor
