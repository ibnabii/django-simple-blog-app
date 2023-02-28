from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView

from .forms import NewEntryForm
from .models import Entry


class RegistrationView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration.html'


class NewEntryView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = NewEntryForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.get_object().author == self.request.user

    model = Entry
    fields = ('title', 'content')
    template_name = 'entry_form.html'


class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    def test_func(self):
        return self.get_object().author == self.request.user

    model = Entry
    success_url = reverse_lazy('entry-owned')
    template_name = 'entry_delete.html'


class OwnedEntriesView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'home.html'

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class AuthorsEntriesView(ListView):
    model = Entry
    template_name = 'home.html'

    def get_queryset(self):
        return self.model.objects.filter(author=self.kwargs['pk'])
