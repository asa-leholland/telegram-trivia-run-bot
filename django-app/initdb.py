from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Initialize the database on container startup'

    def handle(self, *args, **options):
        self.stdout.write('Running migrations...')
        call_command('makemigrations')
        call_command('migrate')
        self.stdout.write('Migrations completed successfully.')

        # Add additional code here if needed