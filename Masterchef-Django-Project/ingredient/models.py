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
    
class categories(models.Model):
  grains_and_flours = models.CharField(max_length=100)
  nuts_and_seeds = models.CharField(max_length=100)
  sweeteners = models.CharField(max_length=100)
  dairy_and_egg_products = models.CharField(max_length=100)
  proteins = models.CharField(max_length=100)
  condiments_and_sauces = models.CharField(max_length=100)
  herbs_spices_and_seasonings = models.CharField(max_length=100)
  fruits = models.CharField(max_length=100)
  vegetables = models.CharField(max_length=100)
  miscellaneous = models.CharField(max_length=100)

  def __str__(self):
      return "Food Categories"