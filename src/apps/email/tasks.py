from django.core.mail import send_mail
from django.conf import settings
from celery import Task


class BaseEmailSenderTask(Task):

    email_host: str = settings.EMAIL_HOST_USER

    operation_name: str = ""

    def pre_run(self, *args, **kwargs):
        return False

    def run(self, *args, **kwargs):
        """
        def run(self, **payment_kwargs):
            response = self.make_request(**payment_kwargs)
            result = self.process_response(response)
            return result
        """
        pre_result = self.pre_run(*args, **kwargs)

        if pre_result:
            return pre_result

        recepients = kwargs['email']
        if isinstance(recepients, str):
            recepients = recepients.split(',')

        email_subject = kwargs['subject']
        email_text = kwargs['text']

        send_mail(
            subject=email_subject,
            message=email_text,
            from_email=self.email_host,
            recipient_list=recepients
        )

        return self.finalize_task_response(recepients)

    def finalize_task_response(self, recepients):
        return {
            'recepients': recepients,
            'status': True,
        }
