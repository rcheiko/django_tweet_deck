import tweepy, os

#Application key
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN =  os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET =  os.getenv("ACCESS_TOKEN_SECRET")

BEARER_TOKEN = os.getenv("BEARER_TOKEN")

CLIENT_ID =  os.getenv("CLIENT_ID")
CLIENT_SECRET =  os.getenv("CLIENT_SECRET")

def get_api(request):
	oauth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
	access_key = request.session['access_token_client']
	access_secret = request.session['access_token_secret_client']
	oauth.set_access_token(access_key, access_secret)
	api = tweepy.API(oauth)
	return api

def get_my_info(request):
	api = get_api(request)
	access_key = request.session['access_token_client']
	access_secret = request.session['access_token_secret_client']

	client = tweepy.Client(
		bearer_token=BEARER_TOKEN,
		consumer_key=API_KEY,
		consumer_secret=API_KEY_SECRET,
		access_token=access_key,
		access_token_secret=access_secret
	)

	user = client.get_me()
	user = api.get_user(screen_name=user.data)
	return user

def get_just_api(request):
	oauth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
	oauth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(oauth)
	return api