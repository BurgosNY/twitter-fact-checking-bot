import tweepy
import time
from mongoengine import NotUniqueError
import pendulum
from models import Tweet, TwitterUser


def parse_tweet_url(tweet_json):
    try:
        url = tweet_json['entities']['urls'][0]['expanded_url']
        cleaned_url = url.split('?')[0]
    except IndexError:
        cleaned_url = 'https://www.twitter.com'
    return cleaned_url


# Returns the last tweet stored in the database related to a given URL
def last_tweet_id(link):
    if Tweet.objects(fake_news_url=link).count() == 0:
        return None
    else:
        return Tweet.objects(fake_news_url=link).order_by('-created_at')[0].id_str


# Helper function to find users with the most followings that shared the story
def find_top_hoaxers(fake_news_url):
    Tweet.objects(fake_news_url=fake_news_url).order_by('-followers_count')


class TwitterBot:

    'Interacts with the Twitter API and the Tweets database'

    def __init__(self, access_token, access_token_secret,
                 consumer_key, consumer_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self._api = tweepy.API(auth)

    def search(self, link):
        search_link = link.split('://')[1]
        response = tweepy.Cursor(self._api.search, q=search_link)
        # TO DO: Investigate why Twitter doesn't like https:// links
        last_tweet = last_tweet_id(link)
        found = False
        for page in response.pages():
            while not found:
                for status in page:
                    try:
                        tweet = self.read_status(status, link)
                        if tweet.id_str == last_tweet:
                            found = True
                        else:
                            try:
                                tweet.save()
                            except NotUniqueError:
                                found = True
                    except tweepy.TweepError:
                        # api limit exceeded. Waiting 15 minutes
                        time.sleep(60 * 15)
                        continue

    def read_status(self, status, search_url):
        # A better way to process Tweepy individual results
        nt = status._json
        new_twitter_user = TwitterUser(
            description=nt['user']['description'],
            followers_count=nt['user']['followers_count'],
            friends_count=nt['user']['friends_count'],
            id_str=nt['user']['id_str'],
            location=nt['user']['location'],
            name=nt['user']['name'],
            screen_name=nt['user']['screen_name'],
            verified=nt['user']['verified'],
        )
        new_tweet = Tweet(
            created_at=pendulum.parse(nt['created_at']),
            id_str=nt['id_str'],
            favorite_count=nt['favorite_count'],
            text=nt['text'],
            retweeted=nt['retweeted'],
            retweet_count=nt['retweet_count'],
            link_url=parse_tweet_url(nt),
            fake_news_url=search_url,
            user=new_twitter_user
        )
        return new_tweet

    def tweet_factcheck(self, tweet_id_str, user, message, correct_link):
        message = f'@{user} {message} {correct_link}'
        new = self._api.update_status(message, in_reply_to_status_id=tweet_id_str)
        print('success')
        return new
