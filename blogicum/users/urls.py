from django.contrib.auth.forms import UserCreationForm
from django.urls import path, include, reverse_lazy
from django.views.generic import CreateView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path(
            'users/registration/',
            CreateView.as_view(
                template_name='registration/registration_form.html',
                form_class=UserCreationForm,
                success_url=reverse_lazy('pages:homepage'),
            ),
            name='registration',
        ),
]
