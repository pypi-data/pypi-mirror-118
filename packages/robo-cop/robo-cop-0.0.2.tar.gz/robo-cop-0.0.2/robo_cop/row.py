from __future__ import annotations
import datetime as dt
from twitch import chat


class Row:
    SCHEMA = ['id',
              'login',
              'display_name',
              'type',
              'broadcaster_type',
              'description',
              'profile_image_url',
              'offline_image_url',
              'view_count',
              'created_at',
              'timestamp',
              'message']

    def __init__(self: Row, timestamp: dt.datetime, message: chat.Message):
        #  User info
        data = message.user.data
        self.id = data['id']
        self.login = data['login']
        self.display_name = data['display_name']
        self.type = data['type']
        self.broadcaster_type = data['broadcaster_type']
        self.description = data['description']
        self.profile_image_url = data['profile_image_url']
        self.offline_image_url = data['offline_image_url']
        self.view_count = data['view_count']
        self.created_at = data['created_at']

        # Message info
        self.timestamp = timestamp.ctime()
        self.message = message.text

    def to_array(self: Row) -> list:
        return [self.id,
                self.login,
                self.display_name,
                self.type,
                self.broadcaster_type,
                self.description,
                self.profile_image_url,
                self.offline_image_url,
                self.view_count,
                self.created_at,
                self.timestamp,
                self.message]

    def __str__(self: Row) -> str:
        return ', '.join(self.to_array())
