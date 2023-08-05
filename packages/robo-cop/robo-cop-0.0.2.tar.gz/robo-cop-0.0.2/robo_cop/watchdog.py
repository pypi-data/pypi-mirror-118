from __future__ import annotations
import csv
import twitch
import datetime as dt
from os import path
from .row import Row


class Watchdog:
    def __init__(self: Watchdog,
                 client_id: str,
                 client_secret: str,
                 client_username: str,
                 log_file: str = './{}-chat-history.csv',
                 use_cache: bool = False,
                 cache_duration: dt.timedelta = dt.timedelta(minutes=1),
                 handle_rate_limit: bool = True):
        self.username = client_username
        self.log_file = log_file

        self.session = twitch.Helix(client_id,
                                    client_secret,
                                    use_cache=use_cache,
                                    cache_duration=cache_duration,
                                    handle_rate_limit=handle_rate_limit)

    def __generate_log_file(self: Watchdog):
        if(not path.exists(self.log_file)):
            with open(self.log_file, 'w') as file:
                file.write(','.join(Row.SCHEMA) + '\n')

    @property
    def oauth_token(self: Watchdog) -> str:
        return 'oauth:421gs94if3pnu04gwk7h4qrru6qwpw'
        # return f'oauth:{self.session.api.bearer_token.split(" ")[1]}'

    def handle_message(self: Watchdog, message: twitch.chat.Message):
        timestamp = dt.datetime.now()
        row = Row(timestamp, message)

        print(f'[{timestamp}]: Message from {row.display_name} {len(row.message)} chars long!')

        with open(self.log_file, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(row.to_array())

    def watch(self: Watchdog, channel_name: str):
        # Update hte log file name to include the channel name
        self.log_file = self.log_file.format(channel_name)

        # Add the pound to the channel name if not included
        if(not channel_name.startswith('#')):
            channel_name = '#' + channel_name

        # Open the log file if it doesn't already exist
        self.__generate_log_file()

        chat = twitch.Chat(channel=channel_name,
                           nickname=self.username,
                           oauth=self.oauth_token,
                           helix=self.session)
        chat.subscribe(self.handle_message)
