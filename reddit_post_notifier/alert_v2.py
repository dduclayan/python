"""
This script will scrape hot submissions in a subreddit you choose and alert you via discord webhook
if a submission with your keyword is found in the post title.

What you need for this script to run:
1. A reddit api client_id and client_secret. How-to: https://tinyurl.com/j4m4nusj
2. A discord server and webhook url. How-to: https://tinyurl.com/2csat5ps

API LIMITS!!!
60 requests per min
100 items per request


@author: Devin Duclayan
"""
import logging
from logging.handlers import RotatingFileHandler
logging.basicConfig(handlers = [RotatingFileHandler('/path/to/your/reddit_api.log',
                    maxBytes = 1000,
                    backupCount = 10)],
                    format = '%(asctime)s | %(levelname)s: %(message)s',
                    datefmt = '%Y-%m-%d %H:%M:%S',
                    level = logging.INFO)
import praw
import requests


def authenticate():
    logging.info('Authenticating...')
    try:
        # you could also store these credentials in a 'praw.ini' file in the 
        # current working directory as your script
        reddit = praw.Reddit(client_id = 'xxx',
                             client_secret = 'xxx',
                             user_agent = 'windows:post-notifier:v1')
        if reddit.read_only:
            logging.info('Authentication Successful!\n')
            return reddit
        else:
            logging.info('Authentication not successful.')
    except:
        logging.error('An error occurred.')
        raise 


def search_posts_for_keyword(subreddit_name, *args):
    """
    

    Parameters
    ----------
    subreddit_name : string
        Name of the subreddit you want to search.
        e.g. http://reddit.com/gundeals
        The subreddit would be 'gundeals'.
    *args : string(s)
        Keyword(s) to look for in the submission title.
        e.g. "glock19", "ar15", "mossberg"

    Returns
    -------
    A notification via discord webhook.

    """
    instance = authenticate()
    sub = instance.subreddit(subreddit_name)
    found_at_least_one_post = False

    for submission in sub.hot(limit=100):
        title = submission.title.lower()
        url = submission.url
        reddit_url = 'https://reddit.com/' + str(submission)
        
        for keyword in args: 
            if keyword in title:
                logging.info('Success! Found post:\n\n%s', title)
                logging.info('url --> %s\n', url)
                found_at_least_one_post = True
                discord_notify(url, title, reddit_url)

    if found_at_least_one_post == False:
        logging.info('Nothing found!')
            
    
def discord_notify(url, post_name, reddit_url):
    webhook_url = 'www.yourdiscordwebhookurl.com'
    
    embed = {
        "description": "Check out this post <@yourlongdiscordid>!",
        "title": "Zastava m70 notification",
        "fields": [
            {
                "name": "post",
                "value": post_name,
                "inline": True,
            },
            {
                "name": "link to item",
                "value": url,
                "inline": True,
            },
            {
                "name": "post comments",
                "value": reddit_url,
            },
        ],
        "image": {
            "url": 'https://static.wikia.nocookie.net/cswikia/images/d/dc/Csgo_chooseteam_Terror.png/revision/latest/scale-to-width-down/365?cb=20151203221253'
        },
        "allowed_mentions": {
            "parse": ['roles'],
            "users": ["yourlongdiscordid"],
        },
    }
        
    data = {
        "content": "ALERT!",
        "username": "notification_bot",
        "embeds": [
            embed
            ],
        }
    
    result = requests.post(webhook_url, json=data)
    if 200 <= result.status_code < 300:
        logging.info(f'Webhook sent {result.status_code}')
        logging.info('==================================')
    else:
        logging.info(f'Not sent with {result.status_code}, response:\n{result.json()}')


def main():
    search_posts_for_keyword('gundeals', 'm70', 'zpapm70')


if __name__ == '__main__':
    main()
