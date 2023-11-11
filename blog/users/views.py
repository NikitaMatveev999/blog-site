from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views import generic
from django.urls import reverse_lazy
from .forms import SignUpForm


class RegistrationView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        valid = super(RegistrationView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        try:
            new_user = authenticate(username=username, password=password)
            if new_user is not None:
                login(self.request, new_user)
            else:
                messages.error(self.request, 'Ошибка регистрации. Попробуйте еще раз.')
                return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, 'Ошибка регистрации. Попробуйте еще раз.')
        return valid
