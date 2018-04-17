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
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=180)
    author = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True)
    post_type = models.CharField(max_length=16, choices=post_types, null=True, default='poll')
    url = models.URLField(blank=True)
    choice1 = models.CharField(max_length=90, null=True)
    choice2 = models.CharField(max_length=90, null=True)
    choice3 = models.CharField(max_length=90, null=True)
    choice4 = models.CharField(max_length=90, null=True)
    rating = models.DecimalField(decimal_places=2, max_digits=3, default=0)
    post_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('post_date',)


class Comment(models.Model):
    """Capture the comments of a given post"""

    comment_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True,
                               related_name='comment_author')
    post = models.ForeignKey(Post, blank=False, on_delete="CASCADE")

    content = models.CharField(max_length=512, null=True)

    date = models.DateTimeField(auto_now=True)
