import time

from db_utils import is_open_session_exists
from slackclient import SlackClient

SLACK_BOT_TOKEN = '<your slack bot token here>'
SLACK_BOT_NAME = '<your slack bot name here>'

def get_slack_bot_id(bot_name):
    if __name__ == "__main__":
        api_call = slack_client.api_call('users.list')
        if api_call.get('ok'):
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == bot_name:
                    print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
                    return user.get('id')
        else:
            print('could not find bot user with the name ' + bot_name)
    return None

BOT_ID = get_slack_bot_id(SLACK_BOT_NAME)
AT_BOT = '<@' + BOT_ID + '>'
EXAMPLE_COMMAND = 'free'

slack_client = SlackClient(SLACK_BOT_TOKEN)

def handle_command(command, channel):
    response = 'Hello! I am the ping pong bot! Ask me if the table is free by typing - \"free?\"'
    if EXAMPLE_COMMAND in command.lower():
        if is_open_session_exists():
            response = 'Sorry, someone is playing right now... Try again later!'
        else:
            response = 'Free to play! enjoy :)'
    slack_client.api_call('chat.postMessage', channel=channel, text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print(SLACK_BOT_NAME + ' connected and running')
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print('connection failed, invalid Slack token or bot ID?')
