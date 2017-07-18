import RPi.GPIO as GPIO
import time

from db_utils import setup_database, handle_motion_detected, handle_no_motion

OBSTACLE_PIN = 11

# The maximum time in seconds allowed for a session to be inactive
MAX_SESSION_TIME_IN_SECONDS = 60
# The time window in seconds we are looking for consecutive movement
DETECTION_FRAME_LENGTH_IN_SECONDS = 10
# The threshold that determines if a movement was detected
DETECTION_INCIDENTS_THRESHOLD = 0.7
    
def setup():
    print 'initializing sensor'
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(OBSTACLE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print 'initializing db'
    time.sleep(10)
    setup_database()

def is_motion_detected():
    return (0 == GPIO.input(ObstaclePin))
    
def loop():
    iteration_counter = 0
    detection_counter = 0.0
    print 'started monitoring'
    while True:
        if (iteration_counter >= DETECTION_FRAME_LENGTH_IN_SECONDS):
            if (detection_counter / iteration_counter >= DETECTION_INCIDENTS_THRESHOLD):
                handle_motion_detected()
            else:
                handle_no_motion(DETECTION_FRAME_LENGTH_IN_SECONDS, MAX_SESSION_TIME_IN_SECONDS)
            iteration_counter = 0
            detection_counter = 0.0
        if (is_motion_detected()):
            detection_counter += 1
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
        
