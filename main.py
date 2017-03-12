import twitter
import signal
import sys

from TwitterWalker import TwitterWalker
from TwitterDatasetServer import TwitterDatasetServer

def strip_newlines(str):
    return str.replace('\n', '').replace('\r', '')

twitter_query = ''

api_file_path = 'api_config.txt'
api_file = open(api_file_path, 'r')
api_consumer_key = strip_newlines(api_file.readline())
api_consumer_secret = strip_newlines(api_file.readline())
api_access_token_key = strip_newlines(api_file.readline())
api_access_token_secret = strip_newlines(api_file.readline())
api_file.close()

query_file_path = 'query.txt'
query_file = open(query_file_path, 'r')
twitter_query = strip_newlines(query_file.readline())
query_file.close()

twit_api = twitter.Api(consumer_key=api_consumer_key,
                       consumer_secret=api_consumer_secret,
                       access_token_key=api_access_token_key,
                       access_token_secret=api_access_token_secret)

server = TwitterDatasetServer(api=twit_api, query=twitter_query)

def sigint_handler(_signo, _stack_frame):
    print('stopping server...')
    server.notify_stop()

signal.signal(signal.SIGINT, sigint_handler)

server.operate()