from django.views.generic import CreateView
from .forms import ContactForm
from .models import Contact
from .tasks import send_email


class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = '/'
    template_name = 'contact/contact.html'

    def form_valid(self, form):
        form.save()
        send_email.delay(form.instance.user_email)
        return super().form_valid(form)
