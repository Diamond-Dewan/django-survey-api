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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    @property
    def get_question_title(self):
        return self.title


class Answer(models.Model):
    """
    As there is only two possible answers
    """
    ANS_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    choice = models.CharField(max_length=3, choices=ANS_CHOICES)

    def __str__(self):
        return self.user.username+": "+self.choice

    @property
    def question_title(self):
        return self.question.get_question_title

    @property
    def user_name(self):
        return self.user.get_username()

