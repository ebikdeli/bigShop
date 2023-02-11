from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django_quill.fields import QuillField


class ContactUs(models.Model):
    "Model to receive feedback from registered or unregistered users"
    name = models.CharField(verbose_name=_('name'), max_length=50)
    subject = models.CharField(verbose_name=_('subject'), max_length=200)
    message = models.TextField(verbose_name=_('message'))
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL,
                             related_name='contact_us_user',
                             blank=True,
                             null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From {self.name}: {self.subject}'


class FAQ(models.Model):
    """Model to create or update FAQ (Frequently Asked Question)"""
    question = QuillField(verbose_name=_('question'))
    answer = QuillField(verbose_name=_('answer'))

    def __str__(self):
        return f'FAQ ({self.id})'
