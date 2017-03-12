import math
import time
import os.path

from TwitterWalker import TwitterWalker
from TwitterDataset import TwitterDataset

class TwitterDatasetServer:
    def __init__(self, **kwargs):
        self.api = kwargs.get('api')
        self.query = kwargs.get('query')
        self.root_path = kwargs.get('root_path', 'server_data')
        if not os.path.exists(self.root_path):
            os.mkdir(self.root_path)
        self.walker = TwitterWalker(root_path=self.root_path, api=self.api, query=self.query)
        self.dataset = TwitterDataset(root_path=self.root_path+'/dataset')
        self.stop = False
    def operate(self):
        iter = 0
        while not self.stop:
            for j in range(10):
                self.step()
                iter += 1
                time.sleep(4)
            self.save()
            print('iteration ' + str(iter) + ', dataset size: %s train, %s test' % self.dataset.sizes())
    def filter_tweets(self, tweets):
        train_tweets = []
        test_tweets = []
        for tweet in tweets:
            if tweet.retweeted_status == None and (not tweet.retweeted) and tweet.media != None:
                if tweet.user.followers_count > 400:
                    train_tweets.append(tweet)
                else:
                    test_tweets.append(tweet)
        return train_tweets, test_tweets
    def step(self):
        tweets = self.walker.next()
        train_tweets, test_tweets = self.filter_tweets(tweets)
        for tweet in train_tweets:
            self.dataset.add_tweet('train', tweet)
        for tweet in test_tweets:
            self.dataset.add_tweet('test', tweet)
    def save(self):
        self.dataset.save()
        self.walker.save()
    def notify_stop(self):
        self.stop = True