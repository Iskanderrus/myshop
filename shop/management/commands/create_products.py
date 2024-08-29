import os
import requests
import tempfile
import pandas as pd
from django.core.management import BaseCommand
from django.core.files import File
from shop.models import Product, Category
from django.utils.text import slugify


class Command(BaseCommand):
    """Command to create new products in the database from an Excel file."""

    help = "Create new products in the database from an Excel file."

    def add_arguments(self, parser):
        parser.add_argument(
            "excel_file",
            type=str,
            help="Path to the Excel file containing product data.",
        )

    def handle(self, *args, **kwargs):
        excel_file = kwargs["excel_file"]
        self.stdout.write(f"Processing file: {excel_file}")

        # Read the Excel file
        df = pd.read_excel(excel_file)

        for index, row in df.iterrows():
            # Extract data from the row
            name = row["name"]
            image_url = row["image"]
            description = row["description"]
            price = row["price"]
            category_name = row["category"]

            # Create a slug from the product name
            slug = slugify(name)

            # Download the image
            image_file = None
            if image_url:
                response = requests.get(image_url)
                if response.status_code == 200:
                    temp_image = tempfile.NamedTemporaryFile(delete=False)
                    temp_image.write(response.content)
                    temp_image.flush()
                    image_file = File(temp_image, name=os.path.basename(image_url))
                else:
                    self.stdout.write(
                        self.style.ERROR(f"Failed to download image for {name}.")
                    )
            
            try:
                category = Category.objects.get(name=category_name.title())
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Category '{category_name}' does not exist. Skipping product '{name}'."))
                continue

            # Create or get the Product instance
            product, created = Product.objects.get_or_create(
                name=name,
                slug=slug,
                description=description,
                price=price,
                category=category,
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Product '{name}' created successfully."))
            else:
                self.stdout.write(self.style.WARNING(f"Product '{name}' already exists."))

            # If image was successfully downloaded, assign it to the product
            if image_file:
                product.image.save(image_file.name, image_file)

            # Save any changes to the product
            product.save()

        self.stdout.write(self.style.SUCCESS("All products processed successfully."))
