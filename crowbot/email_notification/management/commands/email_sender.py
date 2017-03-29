from django.core.management.base import BaseCommand, CommandError
import schedule, time
from datetime import date, timedelta
from backend.models import Semester
from account_system.models import Profile
# from django.conf import settings
# settings.configure()
# from django.core.mail import send_mail
import smtplib
import email.message


class Command(BaseCommand):
    help = 'Sends email'

    def handle(self, *args, **options):

        def send():
            send_list = []

            for profile in Profile.objects.filter(role__exact = Profile.STUDENT):
                send_list.append(profile.user.email)

            TO = send_list
            SUBJECT = 'Update Crowbot page'
            TEXT = "It is now a week before the semester starts, and it's time to update your Crowbot course page.\n" \
                   "\n" \
                   "Greetings from\n" \
                   "The Crowbot Team"

            sender = 'crowbot.ntnu@outlook.com'
            password = 'Crowbot123'

            mail = smtplib.SMTP('smtp-mail.outlook.com', 587)

            mail.ehlo()

            mail.starttls()

            mail.login(sender, password)

            BODY = '\r\n'.join([
                'To: %s' % TO,
                'From: %s' % sender,
                'Subject: %s' % SUBJECT,
                '',
                TEXT
                ])
            try:
                mail.sendmail(sender, send_list, BODY)
            except:
                print("Couldn't send email.")
            finally:
                mail.close()


        def job():
            # sjekke dato i database, finne datoen en uke før, sjekke mot dagens dato
            # vi antar bare en date i semester start, ja?
            for d in Semester.objects.all():
                d.start_date
            send_date = d.start_date - timedelta(days=7)
            if send_date == date.today():
                send()


        schedule.every().day.at("10:30").do(job)

        while True:
            schedule.run_pending()
            time.sleep(50)

