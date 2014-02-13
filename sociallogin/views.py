from django.template import RequestContext
from django.shortcuts import render_to_response
from rauth import OAuth1Service,OAuth2Service
import requests
import urllib
from urlparse import urlparse,parse_qs
from django.http import HttpResponseRedirect
import json

login = 0

facebook = OAuth2Service(
    	client_id='1441600719392672',
    	client_secret='3bfaba15e74908ad56ef83e5df70cb7b',
    	name='Rauth',
    	authorize_url='https://graph.facebook.com/oauth/authorize',
    	access_token_url='https://graph.facebook.com/oauth/access_token',
    	base_url='https://graph.facebook.com/')

google = OAuth2Service(
		client_id='597105662434-3tjpuaebeenv04p2i0ck8djl8376jp23.apps.googleusercontent.com',
    	client_secret='95zTcNUgBF5Xnxe3Y4WLAtHZ',
    	name='google',
    	authorize_url='https://accounts.google.com/o/oauth2/auth',
    	access_token_url='https://accounts.google.com/o/oauth2/token',
    	base_url='https://www.googleapis.com/oauth2/v1/')

twitter = OAuth1Service(
	    name='rauth python',
	    consumer_key='gR4JIHKNqX7NyCW3K2VaKw',
	    consumer_secret='U0Sz9Ie0HwKh5T6OJkao50HWj1YGDpKyJVLfS658',
	    request_token_url='https://api.twitter.com/oauth/request_token',
	    access_token_url='https://api.twitter.com/oauth/access_token',
	    authorize_url='https://api.twitter.com/oauth/authorize',
	    base_url='https://api.twitter.com/1.1/')

request_token = ''
request_token_secret = ''

def LoginTwitter(request):

	global request_token,request_token_secret
	global login
	login = 1
	context = RequestContext(request)
	request_token, request_token_secret = twitter.get_request_token()
	authorize_url = twitter.get_authorize_url(request_token)

	return HttpResponseRedirect(authorize_url)

def LoginFacebook(request):

	global login
	login = 2
	redirect_uri = 'http://localhost:8001/'
	params = {'scope': 'read_stream',
          'response_type': 'code',
          'redirect_uri': redirect_uri}
	url = facebook.get_authorize_url(**params)

	return HttpResponseRedirect(url)

def LoginGoogle(request):

	global login
	login = 3
	print login
	redirect_uri = 'http://localhost:8001/'
	params = {'scope': 'https://www.googleapis.com/auth/userinfo.email',
          'response_type': 'code',
          'redirect_uri': redirect_uri}
	url = google.get_authorize_url(**params)

	return HttpResponseRedirect(url)

def home(request):
	
	global login
	global request_token,request_token_secret
	context = RequestContext(request)
	url = request.get_full_path()
	#print url
	parsed_url = urlparse(url)
	#print parsed_url

	if parsed_url.query == '':
		context_dict = {'message':'Welcome to social login'}
		return render_to_response('index.html', context_dict, context)
		login = 0

	elif 'oauth_verifier' in parsed_url.query:
		verifier = parse_qs(parsed_url.query)['oauth_verifier'][0]
		session = twitter.get_auth_session(request_token,
	                                   request_token_secret,
	                                   method='POST',
	                                   data={'oauth_verifier': verifier})
	 
		params = {'include_rts': 1,  # Include retweets
	          'count': 10}       # 10 tweets
	 
		r = session.get('statuses/home_timeline.json', params=params, verify=True)
		r = r.json()
		print r
		return HttpResponseRedirect('/')

	else:
		q = parse_qs(parsed_url.query)
		foo = str(q['code'][0])
		redirect_uri = 'http://localhost:8001/'
		
		if login == 3:
			data={'code': foo,'redirect_uri': redirect_uri,'grant_type':'authorization_code'}
			response = google.get_raw_access_token(data=data)
			print response
			response = response.json()    
			oauth2_session = google.get_session(response['access_token'])
			user = oauth2_session.get('https://www.googleapis.com/plus/v1/people/me').json()
			print user
		elif login == 2:
			redirect_uri = 'http://localhost:8001/'
			session = facebook.get_auth_session(data={'code': foo,'redirect_uri': redirect_uri})
			print session.get('me').json()['username']
		login = 0
		return HttpResponseRedirect('/')

