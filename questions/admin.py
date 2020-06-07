from django.contrib import admin
from .models import Question, Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', Question.total_votes, 'pub_date']
    list_display_links = ['title']


admin.site.register(Answer)
