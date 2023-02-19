from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=50)
    user_email = models.EmailField()
    text = models.CharField(max_length=300)

    def __str__(self):
        return self.name
