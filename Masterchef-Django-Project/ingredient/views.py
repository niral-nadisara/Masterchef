from django.shortcuts import render
from django.http import HttpResponse
from .models import ingredientItem, recipeItem
import json
from django.views.decorators.csrf import csrf_exempt



# Associate ingredient with a recipe
#r1.list_ingredient.add(i1)

# Create new recipe
#r1 = recipeItem(name="recipe-name", ingredients="ingredient1#ingredient2#ingredient3", directions="step1#step2#step3", img_url="image-url-link")
#r1.save()

# Create ingredients
ingredients_data = [
    #{'name': 'Spinach', 'property': 'Vegetables', 'img_url': 'static/images/spinach.jpg'},
    #{'name': 'Rice', 'property': 'Grains', 'img_url': 'static/images/rice.jpg'},
    # Add more ingredients as needed
]

# Loop through the data and create ingredients
for ingredient in ingredients_data:
    ingredient_obj = ingredientItem.objects.create(
        name=ingredient['name'],
        property=ingredient['property'],
        img_url=ingredient['img_url']
    )
    ingredient_obj.save()


#view for ingredient page
def ingredientView(request):
    all_ingredients = ingredientItem.objects.all()
    return render(request, 'ingredient.html', {'all_ingredients': all_ingredients})

#view for search recipe page
def searchView(request, ingredientId):
    all_recipes= recipeItem.objects.all()
    ingredientObject = ingredientItem.objects.get(id = ingredientId)
    payload = [ingredientObject.name]
    list_recipes = []
    for i in range(0, len(all_recipes)):
      names = []
      ingredients = all_recipes[i].list_ingredient.all()
      for j in range(0, len(ingredients)):
        names.append(ingredients[j].name)
      if set(payload).issubset(set(names)):
        list_recipes.append({'name': all_recipes[i].name,
        'ingredients': all_recipes[i].ingredients.split('#'),
        'directions': all_recipes[i].directions.split('#'),
        'img_url': all_recipes[i].img_url})
    return render(request, 'searchRecipe.html',
    {'ingredientObject': ingredientObject,
    'all_recipes': all_recipes,
    'list_recipes' : list_recipes})

#get ingredient id
def get_ingredientId(request, ingredientName):
  if request.method == 'GET':
    try:
        ingredientId = ingredientItem.objects.get(name = ingredientName).id
        response = json.dumps([{'ingredientId': ingredientId}])
    except:
        response = json.dumps([{'Error': 'No id with that name'}])
  return HttpResponse(response, content_type='text/json')

#get match recipes by list of ingredients
@csrf_exempt
def get_match_recipe(request):
  if request.method == 'POST':
    payload = json.loads(request.body).get('listIngredient')
    try:
      all_recipes = recipeItem.objects.all()
      response = []
      for i in range(0, len(all_recipes)):
        names = []
        ingredients = all_recipes[i].list_ingredient.all()
        for j in range(0, len(ingredients)):
          names.append(ingredients[j].name)
        if set(payload).issubset(set(names)):
          response.append({'name': all_recipes[i].name,
          'ingredients': all_recipes[i].ingredients.split('#'),
          'directions': all_recipes[i].directions.split('#'),
          'img_url': all_recipes[i].img_url})
      response = json.dumps(response)
    except:
      response = json.dumps([{'Error': 'No id with that name'}])
  return HttpResponse(response, content_type='text/json')
