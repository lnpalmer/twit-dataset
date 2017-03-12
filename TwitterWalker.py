import twitter
import os.path

class TwitterWalker:
    def __init__(self, **kwargs):
        self.api = kwargs.get('api')
        self.count = kwargs.get('count', 100)
        self.query = kwargs.get('query')
        self.root_path = kwargs.get('root_path', '.')
        self.file_name = kwargs.get('file_name', 'walker_state.txt')
        if os.path.exists(self.state_path()):
            file = open(self.state_path(), 'r')
            self.cursor_id = int(file.readline())
            self.max_id_historical = int(file.readline())
            file.close()
        else:
            self.cursor_id = 0
            self.max_id_historical = 0
    def next(self):
        try:
            tweets = self.api.GetSearch(raw_query=self.gen_query('older'))
        except twitter.TwitterError as err:
            # something went wrong, probably a rate limiting problem
            return []
        if len(tweets) > 0:
            # earlier tweets were returned, adjust the cursor and finish the step
            self.cursor_id = min([tweet.id for tweet in tweets]) - 1
        else:
            # no tweets were returned, start looking for recent tweets
            tweets = self.api.GetSearch(raw_query=self.gen_query('recent'))
        if len(tweets) > 0:
            self.max_id_historical = max(max([tweet.id for tweet in tweets]), self.max_id_historical)
        return tweets
    def gen_query(self, mode):
        if mode == 'older':
            return self.query + '&result_type=recent&count=' + str(self.count) + '&max_id=' + str(self.cursor_id)
        if mode == 'recent':
            return self.query + '&result_type=recent&count=' + str(self.count) + '&since_id=' + str(self.max_id_historical)
    def state_path(self):
        return self.root_path + '/' + self.file_name
    def save(self):
        file = open(self.state_path(), 'w')
        file.write(str(self.cursor_id) + '\n')
        file.write(str(self.max_id_historical) + '\n')
        file.close()