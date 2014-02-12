from django.template import RequestContext
from django.shortcuts import render_to_response
from rauth import OAuth1Service
import requests
import urllib
from django.http import HttpResponseRedirect


def home(request):
	# print request.get_full_path()
	context = RequestContext(request)
	context_dict = {'message':'Welcome to social login'}
	return render_to_response('index.html', context_dict, context)

def login(request):
	context = RequestContext(request)

	
   	# Get a real consumer key & secret from https://dev.twitter.com/apps/new
	twitter = OAuth1Service(
	    name='rauth python',
	    consumer_key='gR4JIHKNqX7NyCW3K2VaKw',
	    consumer_secret='U0Sz9Ie0HwKh5T6OJkao50HWj1YGDpKyJVLfS658',
	    request_token_url='https://api.twitter.com/oauth/request_token',
	    access_token_url='https://api.twitter.com/oauth/access_token',
	    authorize_url='https://api.twitter.com/oauth/authorize',
	    base_url='https://api.twitter.com/1.1/')
	 
	request_token, request_token_secret = twitter.get_request_token()
	 
	authorize_url = twitter.get_authorize_url(request_token)

	return HttpResponseRedirect(authorize_url)

	# r = urllib.urlopen(authorize_url)
	# r = r.read()

	# verifier = r.url.split("oauth_verifier=",1)[0]
	 
	# # print('Visit this URL in your browser: {url}'.format(url=authorize_url))
	# # pin = read_input('Enter PIN from browser: ')
	 
	# session = twitter.get_auth_session(request_token,
	#                                    request_token_secret,
	#                                    method='POST',
	#                                    data={'oauth_verifier': verifier})
	 
	# params = {'include_rts': 1,  # Include retweets
	#           'count': 10}       # 10 tweets
	 
	# r = session.get('statuses/home_timeline.json', params=params, verify=True)	