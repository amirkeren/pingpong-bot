import RPi.GPIO as GPIO
import time
import datetime
import MySQLdb
import ConfigParser

DEFAULT_TIMESTAMP = '0000-00-00 00:00:00'
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

config = ConfigParser.RawConfigParser()
config.read('/home/pi/motion_detector/config.properties')

DB_HOST = config.get('DatabaseSection', 'database.host');
DB_USER = config.get('DatabaseSection', 'database.user');
DB_PASSWORD = config.get('DatabaseSection', 'database.password');

DB_NAME = 'pingpong'
TABLE_NAME = 'sessions'

def connect_to_db():
    print 'connecting to db'
    conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
    print 'connected'
    return conn

def is_open_session_exists():
    print 'checking if an open session exists'
    open_session_found = False
    conn = connect_to_db()
    x = conn.cursor()
    x.execute('SELECT id FROM ' + TABLE_NAME + ' WHERE end = %s', (DEFAULT_TIMESTAMP))
    data = x.fetchall()
    if (len(data) > 0):
        print 'found an open session'
        open_session_found = True
    else:
        print 'no open session found'
    x.close()
    conn.close()
    return open_session_found

def handle_motion_detected():
    print 'motion detected!'
    conn = connect_to_db()
    x = conn.cursor()
    print 'checking open sessions'
    x.execute('SELECT id FROM ' + TABLE_NAME + ' WHERE end = %s', (DEFAULT_TIMESTAMP))
    data = x.fetchall()
    if (len(data) > 0):
        session_id = data[0][0]
        print 'updating session', session_id, 'in progress'
        update_session(conn, x, session_id)
    else:
        print 'no open sessions found, adding new session'
        add_new_session(conn, x)
    x.close()
    conn.close()
    
def handle_no_motion(DETECTION_FRAME_LENGTH_IN_SECONDS, MAX_SESSION_TIME_IN_SECONDS):
    print 'no motion detected for', DETECTION_FRAME_LENGTH_IN_SECONDS, 'seconds'
    conn = connect_to_db()
    x = conn.cursor()
    print 'checking open sessions'
    x.execute('SELECT id, unix_timestamp(last_updated) FROM ' + TABLE_NAME + ' WHERE end = %s', (DEFAULT_TIMESTAMP))
    data = x.fetchall()
    if (len(data) > 0):
        session_id = data[0][0]
        last_updated = data[0][1]
        print 'session', session_id, 'in progress, checking if it needs to end'
        diff = time.time() - last_updated
        if (diff > MAX_SESSION_TIME_IN_SECONDS):
            close_session(conn, x, session_id)
        else:
            print 'session', session_id, 'did not time out yet'
    else:
        print 'no open sessions'
    x.close()
    conn.close()

def clean_open_sessions(conn, x):
    print 'cleaning open sessions'
    x.execute('DELETE FROM ' + TABLE_NAME + ' WHERE end = %s', (DEFAULT_TIMESTAMP))
    conn.commit()
    print 'cleaned open sessions'
    
def close_session(conn, x, session_id):
    print 'closing session', session_id
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime(TIMESTAMP_FORMAT)
    x.execute('UPDATE ' + TABLE_NAME + ' SET end = %s WHERE id = %s', (timestamp, session_id))
    conn.commit()
    print 'closed session', session_id
    
def update_session(conn, x, session_id):
    print 'updating session', session_id
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime(TIMESTAMP_FORMAT)
    x.execute('UPDATE ' + TABLE_NAME + ' SET last_updated = %s WHERE id = %s', (timestamp, session_id))
    conn.commit()
    print 'updated session', session_id
    
def add_new_session(conn, x):
    print 'adding new session'
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime(TIMESTAMP_FORMAT)
    x.execute('INSERT INTO ' + TABLE_NAME + ' (last_updated) VALUES (%s)', (timestamp))
    conn.commit()
    print 'added new session'

def setup_database():
    conn = connect_to_db()
    x = conn.cursor()
    try:
        x.execute('CREATE DATABASE ' + DB_NAME)
        conn.commit()
    except:
        pass
    try:
        x.execute('''CREATE TABLE IF NOT EXISTS ''' + TABLE_NAME + ''' (
            id smallint unsigned not null auto_increment, 
            start timestamp default current_timestamp, 
            end timestamp default 0, 
            last_updated timestamp, 
            primary key (id)))''')
        conn.commit()
    except:
        pass
    clean_open_sessions(conn, x)
    x.close()
    conn.close()
    
