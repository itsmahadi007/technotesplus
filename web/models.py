from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Notes(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('modified_at',)

    def __str__(self):
        return self.pk


class SharedNotes(models.Model):
    note = models.ForeignKey(Notes, on_delete=models.CASCADE)
    view_permit = models.ManyToManyField(User, related_name='can_view')
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pk
