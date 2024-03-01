# myapp/management/commands/delete_ingredients.py

from django.core.management.base import BaseCommand
from ingredient.models import ingredientItem

class Command(BaseCommand):
    help = 'Delete multiple ingredients from the database'

    def add_arguments(self, parser):
        parser.add_argument('ingredient_names', nargs='+', type=str, help='Names of the ingredients to delete')

    def handle(self, *args, **kwargs):
        ingredient_names = kwargs['ingredient_names']
        for name in ingredient_names:
            try:
                ingredient = ingredientItem.objects.filter(name=name) # filter() for multiple objects, get() for single object
                ingredient.delete()
                self.stdout.write(self.style.SUCCESS(f'Ingredient "{name}" deleted successfully'))
            except ingredientItem.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Ingredient "{name}" does not exist'))
