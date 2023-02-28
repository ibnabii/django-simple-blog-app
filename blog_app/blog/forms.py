from django.forms import ModelForm

from .models import Entry

class NewEntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ('title', 'content')