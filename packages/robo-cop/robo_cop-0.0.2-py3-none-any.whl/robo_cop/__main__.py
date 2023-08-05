from argparse import ArgumentParser
from . import APP_NAME, \
              APP_DESCRIPTION, \
              CLIENT_ID, \
              CLIENT_SECRET, \
              CLIENT_USERNAME, \
              TWITCH_URL
from .watchdog import Watchdog


def main():
    parser = ArgumentParser(APP_NAME, description=APP_DESCRIPTION)
    parser.add_argument('action',
                        type=str,
                        choices=['watch', 'analyze'],
                        help='')
    parser.add_argument('-c', '--channel',
                        dest='channel',
                        type=str,
                        default='the_ivo_robotnic')
    args = parser.parse_args()

    if(args.action == 'watch'):
        watchdog = Watchdog(CLIENT_ID, CLIENT_SECRET, CLIENT_USERNAME)
        print(f'Watching chat for {TWITCH_URL}{args.channel} with oauth token `{watchdog.oauth_token}`')
        watchdog.watch(args.channel)
    elif(args.action == 'analyze'):
        raise NotImplementedError('Analyzing not available yet!')


if __name__ == '__main__':
    main()
