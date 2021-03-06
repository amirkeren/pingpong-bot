import RPi.GPIO as GPIO
import time
import datetime

from db_utils import print_log, setup_database, handle_motion_detected, handle_no_motion

# The physical pin number on the board connected to the DATA output pin of the motion sensor
OBSTACLE_PIN = 11

# The maximum time in seconds allowed for a session to be inactive
MAX_SESSION_TIME_IN_SECONDS = 120
# The time window in seconds we are looking for consecutive movement
DETECTION_FRAME_LENGTH_IN_SECONDS = 60
# The threshold that determines if a movement was detected
DETECTION_INCIDENTS_THRESHOLD = 30

def setup():
    print_log('initializing sensor')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(OBSTACLE_PIN, GPIO.IN)
    print_log('initializing db')
    time.sleep(10)
    # preparing tables, cleaning existing open sessions
    setup_database()

def is_motion_detected():
    return GPIO.input(OBSTACLE_PIN)

def loop():
    iteration_counter = 0
    detection_counter = 0
    print_log('started monitoring')
    while True:
        if iteration_counter >= DETECTION_FRAME_LENGTH_IN_SECONDS:
            if detection_counter >= DETECTION_INCIDENTS_THRESHOLD:
                handle_motion_detected()
            else:
                handle_no_motion(DETECTION_FRAME_LENGTH_IN_SECONDS, MAX_SESSION_TIME_IN_SECONDS)
            iteration_counter = 0
            detection_counter = 0
        if is_motion_detected():
            detection_counter += 1
	    print_log('motion ' + str(detection_counter) + ' detected')
        iteration_counter += 1
        time.sleep(1)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
