from django.contrib import admin

from .models import HashRedirect


class RedirectAdmin(admin.ModelAdmin):
    model = HashRedirect
    readonly_fields = (
        'created_at',
        'modified_at',
        'last_access_at',
        'secret',
        'link'
    )
    list_display = ('description', 'created_at', 'last_access_at', 'url', 'secret')
    list_filter = ('created_at', 'last_access_at',)
    search_fields = ('description', 'secret', )

admin.site.register(HashRedirect, RedirectAdmin)
