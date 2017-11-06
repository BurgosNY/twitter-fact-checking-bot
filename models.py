import settings
from pendulum import now
import mongoengine as mongo

# Initiates the database connection
mongo.connect(
    db=settings.DEFAULT_DB,
    host=settings.MONGODB_URI
)


class TwitterUser(mongo.EmbeddedDocument):
    description = mongo.StringField()
    followers_count = mongo.IntField()
    friends_count = mongo.IntField()
    id_str = mongo.StringField()
    location = mongo.StringField()
    name = mongo.StringField()
    screen_name = mongo.StringField()
    verified = mongo.BooleanField()


class Tweet(mongo.Document):
    created_at = mongo.DateTimeField()
    id_str = mongo.StringField(unique=True)
    favorite_count = mongo.IntField()
    text = mongo.StringField()
    retweeted = mongo.BooleanField()
    retweet_count = mongo.IntField()
    link_url = mongo.URLField()
    fake_news_url = mongo.URLField()
    user = mongo.EmbeddedDocumentField(TwitterUser)
    fact_checked = mongo.BooleanField(default=False)


class TweetFactCheck(mongo.Document):
    fake_news_url = mongo.URLField()
    clicks = mongo.IntField(default=0)
    created_at = mongo.DateTimeField(default=now())
    id_str = mongo.StringField(unique=True)
    replied = mongo.BooleanField(default=False)
    text = mongo.StringField()


class FakeNews(mongo.Document):
    fake_news_url = mongo.URLField(unique=True)
    title = mongo.StringField()
    thumbnail = mongo.URLField()
    facebook_shares = mongo.IntField()
    source = mongo.StringField()
    message_1 = mongo.StringField()
    message_2 = mongo.StringField()
    tweets = mongo.IntField()
    clicks = mongo.IntField()
    replies = mongo.ListField()
    correct_url = mongo.URLField()
    shortened_url = mongo.URLField()
