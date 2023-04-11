from json import loads
from re import search

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect

from .models import HashRedirect


@login_required
def redirect_for_logged_in_user(request, hredirect: HashRedirect):
    if hredirect.is_one_time:
        hredirect.is_active = False
        hredirect.save()
    url, arguments = get_url_arguments(hredirect)
    return redirect(url, **arguments)


@login_required
def login404(request):
    raise Http404

def get_url_arguments(hredirect):
    if hredirect.is_internal:
        arguments = loads(hredirect.internal_arguments.replace('\'', '\"'))
        url = hredirect.url
    else:
        arguments = {}
        if search('^https?:\/\/', hredirect.url):
            url = hredirect.url
        else:
            url = 'https://' + hredirect.url
    return url, arguments

def hash_redirect(request, secrethash):
    try:
        hredirect = HashRedirect.objects.get(Q(secret=secrethash) & Q(is_active=True))
    except HashRedirect.DoesNotExist:
        return login404(request)

    if hredirect.require_login:
        return redirect_for_logged_in_user(request, hredirect)
    else:
        if hredirect.is_one_time:
            hredirect.is_active = False
            hredirect.save()
        return redirect(*get_url_arguments(hredirect))
