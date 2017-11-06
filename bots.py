import settings
from twitter_tools import TwitterBot
from models import Tweet, TweetFactCheck, FakeNews


'''
Updates FakeNews Database
Look at TweetFactCheck database, see what was latest message/url
Create list of what was tweeted (not to repeat)
Look at FakeNews database, select recent posts (with more followers / retweets)
tweet at a person
'''


def update_story_db(url):
    bot = TwitterBot(
        settings.ACCESS_KEY, settings.ACCESS_SECRET,
        settings.CONSUMER_KEY, settings.CONSUMER_SECRET
        )
    bot.search(url)
    total_added = Tweet.objects(fake_news_url=url).count()
    print(f'{total_added} tweets mentioning {url} added.')


def update_fakenews_db():
    urls = FakeNews.objects(fake_news_url__exists=1).values_list('fake_news_url', 'tweets')
    for fake_story, tweets in urls:
        update_story_db(fake_story)
        data_object = FakeNews.objects.get(fake_news_url=fake_story)
        data_object.tweets = Tweet.objects(fake_news_url=fake_story).count()
        data_object.save()


def tweet_fact_check():
    bot = TwitterBot(
        settings.ACCESS_KEY, settings.ACCESS_SECRET,
        settings.CONSUMER_KEY, settings.CONSUMER_SECRET
    )
    query = Tweet.objects(fact_checked=False).order_by(
        '-user__followers_count').values_list(
        'id_str', 'fake_news_url', 'user__screen_name').first()
    fake_story = FakeNews.objects.get(fake_news_url=query[1])
    correct_link = fake_story.shortened_url
    message = fake_story.message_1
    fc_tweet = bot.tweet_factcheck(query[0], query[2], message, correct_link)
    return query


# Different method of getting specific
def specific_tweet_fact_check(fake_news_url):
    from mongoengine.queryset.visitor import Q
    query = Tweet.objects(
        Q(fake_news_url=fake_news_url) &
        Q(fact_checked=False)).order_by(
        '-user__followers_count').values_list(
        'id_str', 'fake_news_url', 'user__screen_name').first()
    return query



    #Tweet.objects(fake_news_url=fake_news_url).order_by('-user__followers_count').values_list('id_str', 'user__followers_count')
