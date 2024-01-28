from os import getenv

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from apps.newsletter.models import Newsletter

User = get_user_model()


class EmailNewsletter:
    """
    This class helps with the distribution of
    Sending email based on streaming invitations.
    """

    def __init__(
        self,
        newsletter: Newsletter = None,
        from_email: str = getenv("EMAIL_HOST_USER"),
        type_content: str = "text/html",
    ):
        self.newsletter = newsletter
        self.from_email = from_email
        self.type_content = type_content

    def _send_email_in_batches(self, recipients_content_list: list):
        """Sends emails to a list of recipients in batches of 50 with HTML content."""

        batch_size = 50
        for i in range(0, len(recipients_content_list), batch_size):
            batch_recipients = recipients_content_list[i : i + batch_size]
            for recipient in batch_recipients:
                msg = EmailMultiAlternatives(
                    subject=recipient["subject"],
                    from_email=self.from_email,
                    to=[recipient["email"]],
                )
                msg.attach_alternative(recipient["text_content"], self.type_content)

                msg.send()

    def send_email_newsletter(self):
        """
        Send email to the user newsletter in batches of 50 recipients per email.
        """

        if self.newsletter:
            newsletter_message = self.newsletter.message
            newsletter_email = self.newsletter.email
            newsletter_title = self.newsletter.title


            recipients_content_dict = [
                {
                    "email": newsletter_email,
                    "subject": _("Newsletter de Century"),
                    "text_content": render_to_string(
                        "newsletter/newsletter.html",
                        context={
                            "message": newsletter_message,
                            "title": newsletter_title,
                        },
                    ),
                }
            ]

            self._send_email_in_batches(recipients_content_dict)
