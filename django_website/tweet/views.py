import tweepy, json
from django.contrib.auth import logout
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .utils import *
from .models import *
from .forms import *

def home(request):
	if check_key(request):
		return render(request, 'home.html', {"logged":True})
	else:
		return render(request, 'home.html', {"logged":False})

def logout_twitter(request):
	if check_key(request):
		request.session.clear()
		logout(request)
	return HttpResponseRedirect(reverse('main'))

def auth(request):
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)

    auth_url = auth.get_authorization_url(True)

    response = HttpResponseRedirect(auth_url)
    request.session['request_token'] = auth.request_token
    return response

def connected(request):
	try:
		verifier = request.GET.get('oauth_verifier')
		oauth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
		token = request.session.get('request_token')
		request.session.delete('request_token')
		oauth.request_token = token
		try:
			oauth.get_access_token(verifier)
		except ValueError:
			print('Error, failed to get access token')

		request.session['access_token_client'] = oauth.access_token
		request.session['access_token_secret_client'] = oauth.access_token_secret

		user = get_my_info(request)
		userExist = User_tweet.objects.filter(author_id=user.id).count()
		if userExist == 0:
			u = User_tweet(
				author_id=user.id,
				access_key=oauth.access_token,
				access_secret=oauth.access_token_secret
			)
			u.save()
		response = HttpResponseRedirect(reverse('profile'))
		return response
	except tweepy.errors.TweepyException:
		response = HttpResponseRedirect(reverse('main'))
		return response

def profile(request):
	if check_key(request):
		user = get_my_info(request)
		return render(request, 'profile.html', {'user':user})
	else:
		return HttpResponseRedirect(reverse('main'))

def permission_tweet(request):
	if check_key(request):
		api = get_just_api(request)
		info = get_my_info(request)

		user = User_tweet.objects.get(author_id=info.id)

		NameOfUserPermission = []
		perm_all = user.perm.all()
		for i in perm_all:
			get_user = api.get_user(user_id=i.author_gived.author_id)
			NameOfUserPermission.append(get_user.screen_name)

		if request.method == "POST":
			form = GivePerm(request.POST)
			if form.is_valid():
				user_perm = form.cleaned_data['user']

				api = get_just_api(request)

				try:
					get_user = api.get_user(screen_name=user_perm)
				except tweepy.errors.TweepyException:
					return render(request, "permission.html", {"form":form, "login":"User need to log minimum 1 time", "UserPerm":NameOfUserPermission})
				if User_tweet.objects.filter(author_id=get_user.id).count() == 0:
					return render(request, "permission.html", {"form":form, "login":"User need to log minimum 1 time", "UserPerm":NameOfUserPermission})
				
				user_gived = User_tweet.objects.get(author_id=get_user.id) # GET USER_GIVED_PERMISSION
				user = User_tweet.objects.get(author_id=info.id) # GET USER WHO GIVE THE PERMISSION
				all_user_gived_perm = user.perm.all()

				for i in all_user_gived_perm:
					if i.author_gived.author_id == str(get_user.id):
						return render(request, "permission.html", {"form":form, "alreadyADD":"You have already add this person to the list.", "UserPerm":NameOfUserPermission})
				user.perm.create(author_gived=user_gived)
			return render(request, "permission.html", {"form":form, "UserPerm":NameOfUserPermission})
		else:
			form = GivePerm()
			return render(request, "permission.html", {"form":form, "UserPerm":NameOfUserPermission})	
	else:
		return HttpResponseRedirect(reverse('main'))

def delete_permission(request):
	if request.method == 'POST':
		if check_key(request):
			who = request.POST.get('deleteName')
			api = get_just_api(request)
			info = get_my_info(request)

			get_user_delete = api.get_user(screen_name=who)
			user = User_tweet.objects.get(author_id=info.id)
			for i in user.perm.all():
				if i.author_gived.author_id == str(get_user_delete.id):
					print('remove')
					user.perm.remove(i)
					i.delete()

			data = json.dumps({})
			return HttpResponse(data, content_type="application/json")
		else:
			raise Http404
	else:
		raise Http404
	
def tweet(request):
	if check_key(request):
		user = get_my_info(request)
		user = User_tweet.objects.get(author_id=user.id)
		user_option = []
		try:
			all_user_tweet = Permission.objects.filter(author_gived=user)
			for i in all_user_tweet:
				api = get_just_api(request)
				owner_user_tweet = User_tweet.perm.through.objects.get(permission_id=i.id)
				owner_user_tweet = User_tweet.objects.get(id=owner_user_tweet.user_tweet_id)
				get_user = api.get_user(user_id=owner_user_tweet.author_id) ### TAKE ALL INFORMATIONS OF EVERY USERS ( we need to take each tag of every users )
				user_option.append(get_user.screen_name)
		except Exception as e:
			print(e)
			return render(request, "tweet.html", {"user_option":user_option})
		return render(request, "tweet.html", {"user_option":user_option})
	else:
		return HttpResponseRedirect(reverse('main'))

def form_tweet(request):
	# if request.method == 'POST':
	# 	print('####################')
	# 	# f = Files(file=request.FILES.get('myfile'))
	# 	# f.save()
	# 	# fileData = request.FILES['fd']
	# 	myfile = request.POST.get('form')
	# 	print(myfile)
	# 	# myfile1 = request.POST('myfile')
	# 	# print('MYFILE :', fileData)
	# 	# print('MYFILE :',myfile1)
	# 	# Files.objects.all().delete()
	# 	# print ('f :', f)
	# 	print('####################')
	# 	# return HttpResponseRedirect(reverse('main'))
	# 	data = json.dumps({})
	# 	return HttpResponse(data, content_type="application/json")


	if request.method == 'POST':
		print('####################')
		print('####################')
		if check_key(request):
			who = request.POST.get('selected')
			tweet = request.POST.get('tweet')

			user = get_my_info(request)
			api = get_just_api(request)

			try:
				get_user = api.get_user(screen_name=who) ### TAKE ALL INFORMATIONS OF EVERY USERS ( we need to take each tag of every users )
			except tweepy.errors.TweepyException as e:
				raise Http404

			owner_user = User_tweet.objects.get(author_id=get_user.id)
			res = User_tweet.perm.through.objects.filter(user_tweet_id=owner_user.id)
			for i in res:
				response = Permission.objects.get(id=i.permission_id)
				if str(user.id) == response.author_gived.author_id:
					api = get_just_api(request)
					user_tweet = User_tweet.objects.get(author_id=get_user.id)

					auth = tweepy.OAuth1UserHandler(
				   		API_KEY, API_KEY_SECRET,
				   		user_tweet.access_key, user_tweet.access_secret
					)
					api = tweepy.API(auth)
					api.update_status(tweet)

					data = json.dumps({})
					return HttpResponse(data, content_type="application/json")
			raise Http404
		else:
			return HttpResponseRedirect(reverse('main'))
	else:
		raise Http404

def check_key(request):
	try:
		access_key = request.session.get('access_token_client', None)
		if not access_key:
			return False
	except KeyError:
		return False
	return True