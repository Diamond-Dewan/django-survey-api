from django.db import models
from django.utils.timezone import now


class Question(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name='Published date', auto_now_add=True)

    def __str__(self):
        return self.title

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
    choice = models.CharField(max_length=1, choices=ANS_CHOICES)
    answered_date = models.DateTimeField(default=now)

