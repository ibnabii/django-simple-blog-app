from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import RedirectView

from .models import HashRedirect

class LoggedInRedirectView(RedirectView, LoginRequiredMixin):
    pass


def hash_redirect(request, hash):
    return HttpResponse(
        HashRedirect.objects.get(secret=hash).url
    )

