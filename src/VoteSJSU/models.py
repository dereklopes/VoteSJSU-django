from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=180)
    author = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True)
    post_type = models.CharField(max_length=16, choices=post_types, null=True, default='poll')
    url = models.URLField(blank=True)

    # max of 4 choices on a poll
    choice1 = models.CharField(max_length=90, null=True)
    choice2 = models.CharField(max_length=90, null=True)
    choice3 = models.CharField(max_length=90, null=True)
    choice4 = models.CharField(max_length=90, null=True)

    # Keep track of votes on Post model for easy querying
    rating = models.DecimalField(decimal_places=2, max_digits=3, default=0)
    num_ratings = models.IntegerField(default=0)
    choice1_votes = models.IntegerField(default=0)
    choice2_votes = models.IntegerField(default=0)
    choice3_votes = models.IntegerField(default=0)
    choice4_votes = models.IntegerField(default=0)

    post_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('post_date',)


class Vote(models.Model):
    vote_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    choice = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
