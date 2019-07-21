import argparse
from ConfigParser import ConfigParser

from . import reddit_poll_bot


def build_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-c', '--config')
    parser.add_argument('-t', '--title',
                        help='the title of the reddit post')
    partial_args, _ = parser.parse_known_args()

    parser.add_argument('choices', nargs='*')

    if partial_args.config is not None:
        return parser
    parser = argparse.ArgumentParser(parents=[parser])
    # login args
    parser.add_argument(
        '--reddit-secret',
        help='The secret API key for your bot account')
    parser.add_argument(
        '--reddit-id',
        help='The ID for the API key for your bot account')
    parser.add_argument('-u', '--username')
    parser.add_argument('-p', '--password')

    return parser


def read_config_file(config_file):
    parser = ConfigParser()
    parser.read(config_file)
    return dict(parser.items('reddit_poll_bot'))


def create_client(args):
    if args.config is not None:
        config =read_config_file(args.config)
        rpb = reddit_poll_bot.RedditPollBot(
            user_agent='Reddit poll bot, in use by {}'.format(config['username']),
            **config)

    else:
        rpb = reddit_poll_bot.RedditPollBot(
            username=args.username,
            password=args.password,
            user_agent='Reddit poll bot, in use by {}'.format(args.username),
            client_id=args.reddit_id,
            client_secret=args.reddit_secret
        )
    return rpb


def create_post():
    parser = build_parser()
    parser.add_argument('-b', '--body',
                        help='the body of the reddit post')
    parser.add_argument('-s', '--subreddit',
                        help='the subreddit of the reddit post')
    args = parser.parse_args()
    rpb = create_client(args)
    if not args.choices:
        exit("You must provide at least 1 choice to create a post")
    post = rpb.create_poll(args.subreddit, args.title, args.body, args.choices)
    print(post.url)


def update_post():
    parser = build_parser()
    args = parser.parse_args()
    rpb = create_client(args)
    exit(not bool(rpb.post_votes(args.title, args.choices)))


def delete_post():
    parser = build_parser()
    args = parser.parse_args()
    rpb = create_client(args)
    exit(not bool(rpb.delete_poll(args.title)))
