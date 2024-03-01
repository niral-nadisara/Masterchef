# manage_ingredients.py

from django.core.management.base import BaseCommand
from ingredient.models import ingredientItem

class Command(BaseCommand):
    help = 'Manage ingredients'

    def add_arguments(self, parser):
        parser.add_argument('action', choices=['add', 'delete'], help='Action to perform')
        parser.add_argument('ingredient_names', nargs='+', type=str, help='Names of ingredients')

    def handle(self, *args, **kwargs):
        action = kwargs['action']
        ingredient_names = kwargs['ingredient_names']

        if action == 'add':
            for name in ingredient_names:
                ingredient_item = ingredientItem.objects.create(name=name)
                self.stdout.write(self.style.SUCCESS(f'Ingredient "{name}" added successfully'))
        elif action == 'delete':
            for name in ingredient_names:
                try:
                    ingredient_item = ingredientItem.objects.get(name=name)
                    ingredient_item.delete()
                    self.stdout.write(self.style.SUCCESS(f'Ingredient "{name}" deleted successfully'))
                except ingredientItem.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Ingredient "{name}" not found'))
