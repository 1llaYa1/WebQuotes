from django.db import models
from django.contrib.auth.models import User

class Source(models.Model):
    name = models.CharField(max_length=500, unique=True)
    
    def get_quotes_count(self):
        return Quote.objects.all().filter(source = self).count()

    def __str__(self):
        return self.name

class Quote(models.Model):
    text = models.CharField(max_length=500, unique=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    weight = models.IntegerField(default=100)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name="likes")
    dislikes = models.ManyToManyField(User, related_name="dislikes")

    def is_liked(self, user, quote_id):
        if self.likes.filter(id=quote_id, likes=user).count() != 0:
            return "voted"
        return None

    def is_disliked(self, user, quote_id):
        if self.dislikes.filter(id=quote_id, likes=user).count() != 0:
            return "voted"
        return None
    
    def get_likes(self):
        return self.likes.count()

    def get_dislikes(self):
        return self.dislikes.count()
    
    def get_views(self):
        return self.views

    def __str__(self):
        return self.text