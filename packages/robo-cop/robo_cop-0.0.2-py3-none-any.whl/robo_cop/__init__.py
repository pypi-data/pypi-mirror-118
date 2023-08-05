import os

MAJOR = 0
MINOR = 0
PATCH = 2

APP_NAME = "robo-cop"
APP_DESCRIPTION = "An AI-powered auto-mod for Twitch chat."
APP_AUTHOR = "The_Ivo_Robotnic"
APP_LICENSE = "MIT"
APP_VERSION = f"{MAJOR}.{MINOR}.{PATCH}"
APP_URL = "https://github.com/the-ivo-robotnic/robo-cop"

CLIENT_USERNAME = "robo-cop"
CLIENT_ID = os.environ.get('ROBOCOP_CLIENT_ID')
CLIENT_SECRET = os.environ.get('ROBOCOP_CLIENT_SECRET')

TWITCH_URL = 'https://twitch.tv/'
