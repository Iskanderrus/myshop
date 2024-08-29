from django.core.management import BaseCommand

from shop.models import Category


class Command(BaseCommand):
    """Command to create new categories in the database."""

    help = "Create new categories in the database."

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating categories...")

        categories = ["coffee", "candies", "cheese", "helva"]
        counter = 0
        for category in categories:
            try:
                Category.objects.create(name=category.title(), slug=category)
                counter += 1
            except:
                self.stdout.write(
                    self.style.ERROR(f"Error creating category: {category}")
                )

        self.stdout.write(
            self.style.SUCCESS(f"{counter} categories created successfully.")
        )
