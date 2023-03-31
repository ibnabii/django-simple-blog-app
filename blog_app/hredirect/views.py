from json import loads
from re import search

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import RedirectView

from .models import HashRedirect


@login_required
def redirect_for_logged_in_user(request, url, arguments):
    return redirect(url, **arguments)


@login_required
def login404(request):
    raise Http404


def hash_redirect(request, secrethash):
    try:
        hredirect = HashRedirect.objects.get(secret=secrethash)
    except HashRedirect.DoesNotExist:
        return login404(request)

    if hredirect.is_internal:
        arguments = loads(hredirect.internal_arguments.replace('\'', '\"'))
        url = hredirect.url
    else:
        arguments = {}
        if search('^https?:\/\/', hredirect.url):
            url = hredirect.url
        else:
            url = 'https://' + hredirect.url



    if hredirect.require_login:
        return redirect_for_logged_in_user(request, url, arguments)
    else:
        return redirect(url, arguments)
