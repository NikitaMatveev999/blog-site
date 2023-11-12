from django.test import TestCase, Client
from django.urls import reverse
from .models import Contact
from .forms import ContactForm


class ContactCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.contact_data = {
            'name': 'Test User',
            'user_email': 'test@example.com',
            'text': 'This is a test message',
        }

    # def test_contact_form_valid(self):
    #     response = self.client.post(reverse('contact_form'), data=self.contact_data)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(Contact.objects.filter(name='Test User').exists())

    def test_contact_form_invalid(self):
        invalid_data = self.contact_data.copy()
        invalid_data['user_email'] = 'invalid_email'
        form = ContactForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_contact_form_view(self):
        response = self.client.get(reverse('contact_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')
