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

def print_log(msg):
    st = datetime.datetime.fromtimestamp(time.time()).strftime(TIMESTAMP_FORMAT)
    print st, msg

def connect_to_db():
    print_log('connecting to db')
    conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
    print_log('connected')
    return conn

def is_open_session_exists():
    print_log('checking if an open session exists')
    open_session_found = False
    conn = connect_to_db()
    x = conn.cursor()
    x.execute('SELECT id FROM ' + TABLE_NAME + ' WHERE end = %s', (DEFAULT_TIMESTAMP))
    data = x.fetchall()
    if (len(data) > 0):
        print_log('found an open session')
        open_session_found = True
    else:
        print_log('no open session found')
    x.close()
    conn.close()
    return open_session_found

def handle_motion_detected():
    print_log('motion detected!')
    conn = connect_to_db()
    x = conn.cursor()
    print_log('checking open sessions')
    x.execute('SELECT id FROM ' + TABLE_NAME + ' WHERE end = %s', (DEFAULT_TIMESTAMP))
    data = x.fetchall()
    if (len(data) > 0):
        session_id = data[0][0]
        print_log('updating session ' + str(session_id) + ' in progress')
        update_session(conn, x, session_id)
    else:
        print_log('no open sessions found, adding new session')
        add_new_session(conn, x)
    x.close()
    conn.close()
    
def handle_no_motion(DETECTION_FRAME_LENGTH_IN_SECONDS, MAX_SESSION_TIME_IN_SECONDS):
    print_log('no motion detected for ' + str(DETECTION_FRAME_LENGTH_IN_SECONDS) + ' seconds')
    conn = connect_to_db()
    x = conn.cursor()
    print_log('checking open sessions')
    x.execute('SELECT id, unix_timestamp(last_updated) FROM ' + TABLE_NAME + ' WHERE end = %s', (DEFAULT_TIMESTAMP))
    data = x.fetchall()
    if (len(data) > 0):
        session_id = data[0][0]
        last_updated = data[0][1]
        print_log('session ' + str(session_id) + ' in progress, checking if it needs to end')
        diff = time.time() - last_updated
        if (diff > MAX_SESSION_TIME_IN_SECONDS):
            close_session(conn, x, session_id)
        else:
            print_log('session ' + str(session_id) + ' did not time out yet')
    else:
        print_log('no open sessions')
    x.close()
    conn.close()

def clean_open_sessions(conn, x):
    print_log('cleaning open sessions')
    x.execute('DELETE FROM ' + TABLE_NAME + ' WHERE end = %s', (DEFAULT_TIMESTAMP))
    conn.commit()
    print_log('cleaned open sessions')
    
def close_session(conn, x, session_id):
    print_log('closing session ' + str(session_id))
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime(TIMESTAMP_FORMAT)
    x.execute('UPDATE ' + TABLE_NAME + ' SET end = %s WHERE id = %s', (timestamp, session_id))
    conn.commit()
    print_log('closed session ' + str(session_id))
    
def update_session(conn, x, session_id):
    print_log('updating session ' + str(session_id))
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime(TIMESTAMP_FORMAT)
    x.execute('UPDATE ' + TABLE_NAME + ' SET last_updated = %s WHERE id = %s', (timestamp, session_id))
    conn.commit()
    print_log('updated session ' + str(session_id))
    
def add_new_session(conn, x):
    print_log('adding new session')
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime(TIMESTAMP_FORMAT)
    x.execute('INSERT INTO ' + TABLE_NAME + ' (last_updated) VALUES (%s)', (timestamp))
    conn.commit()
    print_log('added new session')

def setup_database():
    conn = connect_to_db()
    x = conn.cursor()
    try:
        x.execute('CREATE DATABASE ' + DB_NAME)
        conn.commit()
    except:
        pass
    try:
	cmd = '''CREATE TABLE IF NOT EXISTS ''' + DB_NAME + '''.''' + TABLE_NAME + ''' (
            id smallint unsigned not null auto_increment, 
            start timestamp default current_timestamp, 
            end timestamp default 0, 
            last_updated timestamp, 
            primary key (id))'''
	x.execute(cmd)
        conn.commit()
    except:
        pass
    clean_open_sessions(conn, x)
    x.close()
    conn.close()
    
