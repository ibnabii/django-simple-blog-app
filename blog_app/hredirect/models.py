from secrets import token_urlsafe
from uuid import uuid4

from django.db import models

from . import settings


class HashRedirect(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    description = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    # is_internal: instead using fixed URL, reverse inside app url
    is_internal = models.BooleanField(default=settings.DEFAULT_INTERNAL)
    is_one_time = models.BooleanField(default=settings.DEFAULT_ONE_TIME)
    # only logged-in users can use this url
    require_login = models.BooleanField(default=settings.DEFAULT_REQUIRE_LOGIN)
    url = models.TextField()
    secret = models.CharField(max_length=255, unique=True, db_index=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    last_access_at = models.DateTimeField(null=True, editable=False)

    def save(self, *args, **kwargs):
        exists = True
        while exists:
            new_secret = token_urlsafe(settings.DEFAULT_URL_LENGTH)
            exists = HashRedirect.objects.filter(secret=new_secret).exists()
        self.secret = new_secret
        super().save(*args, **kwargs)

    def __str__(self):
        if len(self.description):
            return self.description
        return self.url
