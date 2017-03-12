import os
import urllib
import json
import copy
import time

class TwitterDataset:
    def __init__(self, **kwargs):
        self.tweets = {'train': {}, 'test': {}}
        self.root_path = kwargs.get('root_path', 'dataset')
        for dir in (self.root_path, self.root_path + '/train', self.root_path + '/test'):
            if not os.path.exists(dir):
                os.mkdir(dir)
        for subset in ('train', 'test'):
            tweets_path = self.tweets_path(subset)
            if os.path.exists(tweets_path):
                file = open(tweets_path, 'r')
                self.tweets[subset] = json.load(file)
                file.close()
    def tweets_path(self, subset):
        return self.root_path + '/' + subset + '/tweets.json'
    def add_tweet(self, subset, tweet):
        path_base = self.root_path + '/' + subset + '/' + str(tweet.id)
        media_url = tweet.media[0].media_url
        media_ext = media_url.split('.')[-1]
        self.download_media(media_url, path_base + '.' + media_ext)
        self.tweets[subset][str(tweet.id)] = tweet.AsDict()
    def save(self):
        for subset in ('train', 'test'):
            tweets_path = self.tweets_path(subset)
            file = open(tweets_path, 'w')
            json.dump(self.tweets[subset], file)
            file.close()
    def sizes(self):
        return len(self.tweets['train']), len(self.tweets['test'])
    def download_media(self, url, file_path):
        while True:
            try:
                urllib.request.urlretrieve(url=url, filename=file_path)
                return
            except urllib.error.URLError as err:
                print('error encountered fetching media! trying again in 60 s...')
                time.sleep(60) # wait a minute and try again