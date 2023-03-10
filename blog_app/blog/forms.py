from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Entry

class NewEntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ('title', 'content')

        labels = {
            'title': _('Post title'),
            'content': _('Post body')
        }