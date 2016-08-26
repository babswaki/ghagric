from django import forms


class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=200, required=False)
    email = forms.EmailField(max_length=254)
    message = forms.CharField(widget=forms.Textarea)
