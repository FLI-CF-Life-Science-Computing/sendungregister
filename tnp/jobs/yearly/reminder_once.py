from django_extensions.management.jobs import YearlyJob

class Job(YearlyJob):
    help = ""
    def execute(self):
        from django.core import management
        from datetime import date
        from ...models import Dataset
        from django.conf import settings
        from django.core.mail import EmailMultiAlternatives, send_mail
        from django.template.loader import render_to_string
        from django.conf import settings
        import logging
        import sys
        try:
            current_date = date.today()
            # find all objects from class Dataset where disposal_date is today
            datasets = Dataset.objects.filter(reminder_disposal__lte = current_date).filter(status='o')
            # if there are any datasets found create a email message for each dataset and inform the user (added_by)
            if datasets.exists():
                for dataset in datasets:
                    #print(dataset)
                    # create a email message
                    email = EmailMultiAlternatives(
                        subject=f"Reminder Sendungsregister: {dataset.material.name}",
                        body=render_to_string("email/reminder_once.txt", {"dataset": dataset, "domain": settings.DOMAIN ,"admin_contact": settings.ADMIN_CONTACT}),
                        from_email=settings.EMAIL_HOST_USER,
                        to=[dataset.added_by.email],
                    )
                    # send the email
                    email.send()
            #else:
                #logging.error("No datasets found for today's disposal.")
        except Exception as e:
            # send a mail to the admin with the error message
            send_mail(
                "Error Sendungsregister: reminder.py",
                f"An error occurred while processing the disposal job: {str(e)}",
                settings.EMAIL_HOST_USER,
                [settings.TEC_ADMIN_EMAIL],
            )
            # exit the script with an error code 1 to indicate failure
            #logging.error(f"An error occurred while processing the disposal job: {e}")
            sys.exit(1)
