# default values for redirect

# instead using fixed URL, reverse inside app url
DEFAULT_INTERNAL = True

# automatically deactivate redirect after it's been used
# alternatively for internal links they can be deactivated by the target view
DEFAULT_ONE_TIME = False

# does a user need to be logged in to use redirect?
# user will be required to log-in anyway to see 404 error, but setting this to False will let
# anonymous users use redirection.
DEFAULT_REQUIRE_LOGIN = True

# length of a redirect string, do not use more than 255
DEFAULT_URL_LENGTH = 50