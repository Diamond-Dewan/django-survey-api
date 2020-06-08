from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


# token generator
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Question(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    @property
    def total_votes(self):
        return self.answers.count()


class Answer(models.Model):
    """
    As there is only two possible answers
    """
    ANS_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No')
    ]
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.CharField(max_length=1, choices=ANS_CHOICES)
