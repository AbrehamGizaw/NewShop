import subprocess
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from scripts.db_migrator import populate_whyus, populate_vendor_cats, populate_vendors, populate_news, populate_socialmedias

class Command(BaseCommand):
    help = 'Runs both makemigrations and migrate commands at once and updates the db if there is anything to update.'
        
    def populate_superuser(self):
        # creating superuser
        User = get_user_model()
        admin_username = "admin"
        pw = "adminpw"
        if User.objects.filter(username ="admin"):
            self.stdout.write(self.style.WARNING(f"Superuser with a username '{admin_username}' already exists. Skipping creation."))
        else:
            try:# Create the superuser with default values
                User.objects.create_superuser(username=admin_username, password=pw,first_name="Superadmin", last_name="User")
                self.stdout.write(self.style.SUCCESS(f'Successfully created superuser with username ={admin_username} & pw = {pw}.'))
            
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error creating superuser: {e}'))

    def add_arguments(self, parser):
        parser.add_argument('--populate', type=bool, help='Use like --populate=True, to populate initial data.', default=False)
        
    def data_migrator(self):
        
        print("Populating initial data...\n")
        
        self.populate_superuser()
        populate_whyus()

        # populating vendor app models (keep the order )
        populate_vendor_cats()
        populate_vendors()
        populate_news()

        populate_socialmedias()

        print("Data population completed")
        
    def handle(self, *args, **options):
        pop_data = options['populate']
        self.stdout.write("Making migrations to all apps...")
        
        call_command('makemigrations','accounts','core','notifications','vendor', interactive=True)
        self.stdout.write(" \nMigrating...")
        call_command('migrate', interactive=True)
        self.stdout.write(self.style.SUCCESS("\nMigration completed successfully"))
        
        # if want to populate data
        if pop_data:
            self.data_migrator()
        self.stdout.write("\nDB is updated.")


