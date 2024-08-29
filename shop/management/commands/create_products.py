from django.core.management import BaseCommand


class Command(BaseCommand):
    """Command to create new products in the database."""

    help = "Create new products in the database."

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating products...")

        products = {}



        self.stdout.write(self.style.SUCCESS("Products created successfully."))


