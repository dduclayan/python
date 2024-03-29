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
import praw
import requests


def authenticate():
    try:
        print('Authenticating...')
        # creates an instance of the 'Reddit' class so you can do stuff with reddit posts
        reddit = praw.Reddit(client_id = 'xxx',
                              client_secret = 'xxx',
                              user_agent = '<platform>:<script_name>:<version>')
        if reddit.read_only:
            print('Authentication successful!')
            return reddit
        else:
            print('Authentication not successful.')
    except:
        print('An error occurred.')
        raise 


def search_posts_for_keyword(subreddit_name, search_term):
    """


    Parameters
    ----------
    subreddit_name : string
        Name of the subreddit you want to search.
        e.g. http://reddit.com/gundeals
        The subreddit would be 'gundeals'.
    search_term : string
        e.g. "glock19"

    Returns
    -------
    A notification via discord webhook if keyword is found in post.

    """
    instance = authenticate()
    sub = instance.subreddit(subreddit_name)
    found_at_least_one_post = False

    for submission in sub.hot(limit=100):
        title = submission.title.lower()
        url = submission.url
        reddit_url = 'https://reddit.com/' + str(submission)
        
        if search_term in title:
            print(f'Success! Found {title}')
            print(f'{reddit_url}')
            found_at_least_one_post = True
            discord_notify(url, title, reddit_url)
      
    if found_at_least_one_post == False:
        print('Nothing found!')
            
    
def discord_notify(url, post_name, reddit_url):
    webhook_url = 'https://yourdiscordwebhookurl.com'
    
    embed = {
        "description": "Check out this post <@{your long disord id}>!",
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
                "name": "url to comments",
                "value": reddit_url,
            },
        ],
        "image": {
            "url": 'https://static.wikia.nocookie.net/cswikia/images/d/dc/Csgo_chooseteam_Terror.png/revision/latest/scale-to-width-down/365?cb=20151203221253'
        },
        "allowed_mentions": {
            "parse": ['roles'],
            "users": ["<your long discord id>"],
        },
        }
        
    
    data = {
        "content": "ALERT!",
        "username": "custom name",
        "embeds": [
            embed
            ],
        }
    
    result = requests.post(webhook_url, json=data)
    if 200 <= result.status_code < 300:
        print(f'Webhook sent {result.status_code}')
    else:
        print(f'Not sent with {result.status_code}, response:\n{result.json()}')


def main():
    search_posts_for_keyword('gundeals', 'm70')


if __name__ == '__main__':
    main()
