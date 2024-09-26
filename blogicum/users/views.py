from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import ListView, UpdateView

from blog.constants import POST_AMOUNT
from users.forms import User, UserForm, PasswordChangeForm


def login(request):
    template = 'registration/login.html'
    return render(request, template)


class UserDetailView(ListView):
    model = User
    template_name = 'blog/profile.html'
    paginate_by = POST_AMOUNT

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs.get('username'))

        if self.author != self.request.user:
            return User.objects.filter(is_published=True, author=self.author).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        context['user'] = self.request.user
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.user.get_username())

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=kwargs['username'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.user.get_username()})


class UserPasswordChangeView(UserUpdateView):
    form_class = PasswordChangeForm
    model = User
    template_name = 'registration/password_reset_form.html'
