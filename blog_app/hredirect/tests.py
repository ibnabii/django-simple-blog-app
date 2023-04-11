from json import loads

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from .models import HashRedirect

# from django.utils import translation
# translation.activate('PL')
# csrf_client = Client(enforce_csrf_checks=True)


def setup_user(username: str) -> User:
    # setup test user
    user = User.objects.create(username=username)
    user.set_password('12345')
    user.save()
    return user


class HashRedirections(TestCase):
    def check_link_404(self, url):
        c = Client()
        user = setup_user('test_user')

        # user not logged in: should be redirected to login page
        response = c.get(url)
        self.assertRedirects(response, '/login/?next=' + url, target_status_code=302, fetch_redirect_response=False)

        # logged-in user gets 404
        # c.login(username='testuser', password='12345')
        c.force_login(user)
        response = c.get(url)
        self.assertEqual(response.status_code, 404)
        # logout again
        c.logout()
        response = c.get(url)
        self.assertRedirects(response, '/login/?next=' + url, target_status_code=302, fetch_redirect_response=False)
        return True

    def test_wrong_hash(self):
        # url = reverse('hredirect:first', args=['abcd'])
        url = reverse('hredirect:first', kwargs={'secrethash': 'abcd'})
        self.assertEqual(self.check_link_404(url), True)

    def test_inactive_link_with_login(self):
        hr = HashRedirect.objects.create(
            secret='kqweuqwop',
            is_active=False,
            require_login=True,
            is_internal=False,
            url='www.google.com'
        )

        url = reverse('hredirect:first', kwargs={'secrethash': hr.secret})
        self.assertEqual(self.check_link_404(url), True)

    def test_inactive_link_no_login(self):
        hr = HashRedirect.objects.create(
            secret='kqweuqwop',
            is_active=False,
            require_login=True,
            is_internal=False,
            url='www.google.com'
        )

        url = reverse('hredirect:first', kwargs={'secrethash': hr.secret})
        self.assertEqual(self.check_link_404(url), True)

    def test_external_link_no_login(self):
        hr = HashRedirect.objects.create(
            secret='test_external_link_no_login',
            require_login=False,
            is_internal=False,
            url='www.google.com'
        )
        url = reverse('hredirect:first', kwargs={'secrethash': hr.secret})
        c = Client()
        response = c.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://' + hr.url)

    def test_external_link_with_login(self):
        hr = HashRedirect.objects.create(
            secret='test_external_link_with_login',
            require_login=True,
            is_internal=False,
            url='www.google.com'
        )
        url = reverse('hredirect:first', kwargs={'secrethash': hr.secret})
        c = Client()
        response = c.get(url)
        self.assertRedirects(response, '/login/?next=' + url, target_status_code=302)

        c.force_login(setup_user('test_user'))
        response = c.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://' + hr.url)

    def test_internal_link_no_login(self):
        # redirection to internal links works strange in test framework,
        # hence the assertion does not use redirect, result i got was:
        # AssertionError: "/en/redirect/%7B'secrethash':%20'abcd'%7D/" != '/en/redirect/abcd/'
        # - /en/redirect/%7B'secrethash':%20'abcd'%7D/
        # + /en/redirect/abcd/

        hr = HashRedirect.objects.create(
            secret='test_external_link_no_login',
            require_login=False,
            is_internal=True,
            url='hredirect:first',
            internal_arguments='{"secrethash": "abcde"}'
        )
        url = reverse('hredirect:first', kwargs={'secrethash': hr.secret})
        target_url = reverse(hr.url, kwargs=loads(hr.internal_arguments))
        c = Client()
        response = c.get(url)
        self.assertEqual(response.status_code, 302)
        for item in target_url.split('/')[1:-1]:
            # first and last elements are ''
            self.assertIn(item, response.url)

    def test_internal_link_with_login(self):
        # redirection to internal links works strange in test framework,
        # hence the assertion does not use redirect, result i got was:
        # AssertionError: "/en/redirect/%7B'secrethash':%20'abcd'%7D/" != '/en/redirect/abcd/'
        # - /en/redirect/%7B'secrethash':%20'abcd'%7D/
        # + /en/redirect/abcd/

        hr = HashRedirect.objects.create(
            secret='test_external_link_with_login',
            require_login=True,
            is_internal=True,
            url='hredirect:first',
            internal_arguments='{"secrethash": "abcde"}'
        )
        url = reverse('hredirect:first', kwargs={'secrethash': hr.secret})
        target_url = reverse(hr.url, kwargs=loads(hr.internal_arguments))
        c = Client()
        response = c.get(url)
        self.assertRedirects(response, '/login/?next=' + url, target_status_code=302)

        c.force_login(setup_user('test_internal_link_with_login'))
        response = c.get(url)

        self.assertEqual(response.status_code, 302)
        for item in target_url.split('/')[1:-1]:
            # first and last elements are ''
            self.assertIn(item, response.url)

    def test_OTL_ext_no_login(self):
        hr = HashRedirect.objects.create(
            secret='test_OTL_ext_no_login',
            require_login=False,
            is_internal=False,
            is_one_time=True,
            url='www.google.com'
        )

        url = reverse('hredirect:first', kwargs={'secrethash': hr.secret})
        c = Client()
        response = c.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://' + hr.url)

        self.assertEqual(self.check_link_404(url), True)

    def test_OTL_ext_with_login(self):
        hr = HashRedirect.objects.create(
            secret='test_OTL_ext_with_login',
            require_login=True,
            is_internal=False,
            is_one_time=True,
            url='www.google.com'
        )

        url = reverse('hredirect:first', kwargs={'secrethash': hr.secret})
        c = Client()
        response = c.get(url)
        self.assertRedirects(response, '/login/?next=' + url, target_status_code=302)

        # 2nd attempt
        response = c.get(url)
        self.assertRedirects(response, '/login/?next=' + url, target_status_code=302)

        c.force_login(setup_user('test_OTL_ext_with_login'))
        response = c.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://' + hr.url)

        # should no longer be available
        c.logout()
        self.assertEqual(self.check_link_404(url), True)
