from django.db import models

class ingredientItem(models.Model):
  name = models.TextField()
  property = models.TextField()
  img_url = models.TextField()

class recipeItem(models.Model):
  name = models.TextField()
  ingredients = models.TextField()
  directions = models.TextField()
  img_url = models.TextField()
  list_ingredient = models.ManyToManyField(ingredientItem)

class ChefRecipe(models.Model):
    cuisine = models.TextField()
    time = models.TextField()
    steps = models.TextField()
    description = models.TextField()
    ingredients = models.TextField()

    def __str__(self):
        return self.cuisine