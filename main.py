import tweepy
from configparser import ConfigParser
import re


class TweetData(object):
    def __init__(self, configfile, api, user):

        self.user = user
        self.configfile = configfile
        self.api = api
        self.config = ConfigParser()
        self.config.read(configfile)

        auth = tweepy.OAuthHandler(self.config.get(self.api, "consumer_key"),
                                   self.config.get(self.api, "consumer_secret"),
                                  )
        auth.set_access_token(self.config.get(self.api, "token_key"),
                              self.config.get(self.api, "token_secret"),
                             )

        self.client = tweepy.API(auth)

    def get_timeline(self):
        profile = self.client.get_user(self.user)
        timeline = self.client.user_timeline(profile.id)
        return timeline

    def get_tweet_text(self):
        _timeline = self.get_timeline()
        _tweet = _timeline.pop()
        _imgurl = _tweet.extended_entities['media'][0]['media_url']
        _tweet = _tweet.text
        _tweet = _tweet.split(' ')[0:-1]
        _tweet = " ".join(_tweet)
        _tweet = _tweet.replace('\n', ' ')
        _tweet = _tweet.replace('\u2116', '{0}')
        _tweet = _tweet.replace('\u2023', '{1}')
        _tweet = _tweet.format('&#x2116', '&#x2023')
        
        return _tweet


client = TweetData("config.ini", "summon", "ebooks_goetia")

print(client.get_tweet_text())

