from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.shortcuts import render, redirect

from .forms import ContactForm

class HomePage(TemplateView):
    template_name = 'base/index.html'

def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form_full_name = form.cleaned_data.get('full_name')
        form_email = form.cleaned_data.get('email')
        form_message = form.cleaned_data.get('message')

        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = ['ib.waki@yahoo.com']
        contact_message = "{}: {} via {}".format(
            form_full_name,
            form_message,
            form_email)

        send_mail(subject, contact_message, from_email,
                  to_email, fail_silently=False)
        # redirect to a new URL:
        return redirect(request.path)

    return render(request, 'base/form.html', {'form': form})

def about(request):
    about_us = 'This is ib 0242271258'

    return render(request, 'base/about.html', {'about_us': about_us})