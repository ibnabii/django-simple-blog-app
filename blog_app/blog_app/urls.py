from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('redirect/', include('hredirect.urls')),
    path('', include('blog.urls')),
    path('login/', LoginView.as_view(
        template_name='login.html',
        next_page='/'
        ), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('i18n/', include('django.conf.urls.i18n')),
    # prefix_default_language=False
    # enabling line above enforces that english (LANGUAGE_CODE) is enabled. If not the URL i18n patterns fail,
    # so Django Middleware moves to next steps determining the languages and finally fetches the browser header
    # and redirecrts to appropriate language (or defaults to LANGUAGE_CODE)
)
