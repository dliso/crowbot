from django.core.management.base import BaseCommand, CommandError

from backend.models import Question, Answer

class Command(BaseCommand):
    help = 'Empty the Question and Answer tables'

    def handle(self, *args, **options):
        self.stdout.write('Delete all questions and answers? (y/n)')
        ans = input()
        if ans and ans[0] == 'y':
            self.stdout.write('Deleting questions and answers')
            for q in Question.objects.all():
                q.delete()
            for a in Answer.objects.all():
                a.delete()
        else:
            self.stdout.write('Aborting')
