import schedule, time
from datetime import date, timedelta
from backend.models import Semester
# from django.conf import settings
# settings.configure()
from django.core.mail import send_mail
import smtplib

def send():
    """
    content = 'It is a week before the semester starts. Remember to update your Crowbot course page.'

    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login('crowbot.ntnu@gmail.com', 'Crowbot123')

    mail.sendmail('crowbot.ntnu@gmail.com', 'mariefbjordal@hotmail.com', content)

    mail.close()
    """
    send_mail(
        'Subject here',
        'Here is the message.',
        settings.EMAIL_HOST_USER,
        ['mariefbjordal@gmail.com', settings.EMAIL_HOST_USER],
        fail_silently=False,
    )

def job():
    #sjekke dato i database, finne datoen en uke før, sjekke mot dagens dato
    #vi antar bare en date i semester start, ja?
    for d in Semester.objects.all():
        d.start_date()
    send_date = d.start_date + timedelta(days=1)
    if send_date == date.today():
        send()


schedule.every().minute.do(job)

while True:
    schedule.run_pending()
    #time.sleep(86399)
    time.sleep(60)
"""
send_mail(
        'Subject here',
        'Here is the message.',
        settings.EMAIL_HOST_USER,
        ['mariefbjordal@gmail.com', settings.EMAIL_HOST_USER],
        fail_silently=False,
    )

"""




