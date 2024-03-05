from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils.translation import gettext_lazy 




    
class Task(models.Model):
    class Status(models.TextChoices):
        Todo = 'Todo', gettext_lazy ('Todo')
        Done = 'Done', gettext_lazy ('Done')
        Inprogress = 'InPr', gettext_lazy ('InProgress')
        

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    
    status = models.CharField(
        max_length=4,
        choices=Status.choices,
        default=Status.Todo,
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = 'user'
