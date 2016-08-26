from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Comment

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        # fields = '__all__'
        exclude = ['slug', 'pub_date', 'post']
        labels = {
            'full_name': _('Name'),
            'author_email': _('Email'),
            'email': _('Website'),
            'content': _('Comment'),
        }

#
# class ContactForm(forms.Form):
#     full_name = forms.CharField(max_length=200, required=False)
#     email = forms.EmailField(max_length=254)
#     message = forms.CharField(widget=forms.Textarea)
