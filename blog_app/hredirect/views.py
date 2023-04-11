from json import loads
from re import search
from logging import getLogger

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, reverse

import qrcode

from .models import HashRedirect

logger = getLogger('hredirect')

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
    logger.debug(f"Accessing hashredirect: {secrethash}")
    try:
        hredirect = HashRedirect.objects.get(Q(secret=secrethash) & Q(is_active=True))
    except HashRedirect.DoesNotExist:
        logger.debug("Hash not found")
        return login404(request)
    else:
        logger.debug("Hash found")

    if hredirect.require_login:
        return redirect_for_logged_in_user(request, hredirect)
    else:
        if hredirect.is_one_time:
            hredirect.is_active = False
            hredirect.save()
        return redirect(*get_url_arguments(hredirect))

def render_qr_code(request, secrethash):
    # img = qrcode.make(
    #     request.build_absolute_uri(
    #         reverse('hredirect:first', kwargs={'secrethash': secrethash})
    #     )
    # )
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=5,
        border=4,
    )
    qr.add_data(
        request.build_absolute_uri(reverse('hredirect:first', kwargs={'secrethash': secrethash}))
    )
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    response = HttpResponse(content_type="image/png")
    img.save(response, 'PNG')
    return response
