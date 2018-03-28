from django.db import models


class Account(models.Model):
    email = models.EmailField(primary_key=True, default='default@votesjsu.com')
    name = models.CharField(max_length=32, blank=True)
    join_date = models.DateTimeField(auto_now=True)
    points = models.IntegerField(default=0)


class Post(models.Model):
    post_types = (
        ('poll', 'Poll'),
        ('rating', 'Rating'),
    )
    title = models.CharField(max_length=180)
    author = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    post_type = models.CharField(max_length=16, choices=post_types, blank=False, default='poll')
    url = models.URLField()
