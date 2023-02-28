from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy


class Entry(models.Model):
    class Meta:
        ordering = ['-updated']
        verbose_name_plural = 'entries'

    title = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse_lazy('entry-details', kwargs={'pk': self.id})

