from django.core.management.base import BaseCommand, CommandError

import nltk

class Command(BaseCommand):
    help = 'Download the necessary NLTK corpora'

    def handle(self, *args, **options):
        corpora = ['wordnet', 'stopwords', 'punkt', 'averaged_perceptron_tagger']
        for corp in corpora:
            self.stdout.write('Downloading corpora "{:s}"'.format(corp))
            nltk.download(corp)
