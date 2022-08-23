from django.db import models

class User_tweet(models.Model):
    author_id = models.TextField(null=True)
    access_key = models.TextField(null=True)
    access_secret = models.TextField(null=True)
    perm = models.ManyToManyField('Permission')

class Permission(models.Model):
    author_gived = models.ForeignKey(User_tweet, on_delete=models.CASCADE)