from django.core.mail import EmailMessage
import os
import logging

logger = logging.getLogger(__name__)

class Util:
    @staticmethod
    def send_email(data):
        try:
            # Get sender email from environment variables
            email_from = os.environ.get('EMAIL_FROM')
            if not email_from:
                raise RuntimeError("EMAIL_FROM environment variable is not set.")

            # Ensure "to_email" is a list
            to_email = data['to_email']
            if not isinstance(to_email, (list, tuple)):
                to_email = [to_email]

            email = EmailMessage(
                subject=data['subject'],
                body=data['body'],
                from_email=email_from,
                to=to_email,
            )

            # Add support for HTML emails if needed
            if data.get('is_html', False):
                email.content_subtype = 'html'

            # Attach files if provided
            attachments = data.get('attachments', [])
            for attachment in attachments:
                email.attach_file(attachment)

            # Send email
            email.send()
            logger.info(f"✅ Email sent successfully to {', '.join(to_email)}")

        except Exception as e:
            logger.error(f"❌ Failed to send email to {', '.join(to_email)}: {str(e)}", exc_info=True)
            raise
