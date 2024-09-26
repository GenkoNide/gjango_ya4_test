from django.contrib.auth.forms import UserCreationForm
from django.urls import path, include, reverse_lazy
from django.views.generic import CreateView


from users.views import UserUpdateView, UserPasswordChangeView, UserDetailView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('registration/',
         CreateView.as_view(
             template_name='registration/registration_form.html',
             form_class=UserCreationForm,
             success_url=reverse_lazy('pages:homepage'),
         ),
         name='registration',
         ),
    path('<str:username>/',
         UserDetailView.as_view(), name='profile'),

    path('<str:username>/edit/',
         UserUpdateView.as_view(), name='edit_profile'),

    path('<str:username>/edit/password/',
         UserPasswordChangeView.as_view(), name='password_change'),
]
