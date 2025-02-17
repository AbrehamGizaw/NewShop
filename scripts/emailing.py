import threading
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


class ThreadEmailSender(threading.Thread):
    """ Sends emails dynamically using a thread. """

    def __init__(self, template, subject, to_email, params=None, sender_name=None):
        super().__init__()
        self.template = template
        self.subject = subject
        self.to_email = to_email
        self.params = params or {}
        self.sender_name = sender_name or "InternationalB2BVentures"
        self.attachments = []  
        self.result_event = threading.Event()

    def run(self):
        try:
            mail_subject = self.subject
            message = render_to_string(self.template, self.params)
            email_from = getattr(settings, "DEFAULT_FROM_EMAIL", self.sender_name)
            email = EmailMultiAlternatives(mail_subject, message, email_from, [self.to_email], )

            for attachment in self.attachments:
                email.attach(*attachment)

            email.attach_alternative(message, 'text/html')
            email.send(fail_silently=False)
            print(f"Sent activation email to {self.to_email}")
            self.result_event.set()
        except Exception as e:
            print(f'Failed to send email to {self.to_email}: {e}')
            self.result_event.set()