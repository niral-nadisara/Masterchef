from audioop import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ingredientItem, recipeItem, ChefRecipe
import json
from django.core.serializers import serialize
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

def read_ingredient_by_name(request):
    data = ChefRecipe.objects.all()


    if 'q' in request.GET:
        q = request.GET['q']
        query_terms = q.split(",")
        for term in query_terms:
            data = data.filter(ingredients__icontains=term)

    # Convert queryset data to a list of dictionaries
    data_dict_list = []
    for instance in data:
        ingredients_list = [item.strip() for item in instance.ingredients.split(",")]
        ingredients_list = list(ingredients_list)
        items_to_remove = list(q.split(","))
        # print("Initial Ingredients List:", ingredients_list)
        # print("Items to Remove:", items_to_remove)

        # Remove items dynamically using list comprehension
        ingredients_listUpdated = [item for item in ingredients_list if item not in items_to_remove]
        # print("Updated Ingredients List:", ingredients_listUpdated)
        ingredientsMoreNeded = ', '.join([str(elem) for elem in ingredients_listUpdated])
        # print("Updated Ingredients List as str: ", ingredientsMoreNeded)

        instance_dict = {
            'cuisine': instance.cuisine,
            'time': instance.time,
            'ingredients': instance.ingredients,
            'steps': instance.steps,
            'description': instance.description,
            'ingredientsMoreNeded':ingredientsMoreNeded
            # Add other fields as needed
        }
        data_dict_list.append(instance_dict)
        # break;

    # Check if any recipes are found
    if not data_dict_list:
        no_recipes_message = "No recipes found for the provided ingredient(s)."
        return render(request, 'ingredient.html', {'no_recipes_message': no_recipes_message})

    # Paginate the data
    paginator = Paginator(data_dict_list, 10)
    page_number = request.GET.get('page', 1)
    try:
        data = paginator.page(page_number)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    return render(request, 'ingredient.html', {'data': data})

def get_All_Ingredients():
    
    # Retrieve the first n number of records from the ChefRecipe model
    data = ChefRecipe.objects.values_list('ingredients', flat=True)[:10]

    # Initialize a set to store distinct ingredients
    distinct_ingredients = set()

    # Iterate over the ingredients in the first 20 records
    for ingredients in data:
        # Split the ingredients string into a list
        ingredient_list = ingredients.split(',')
        # Add each ingredient to the set of distinct ingredients
        distinct_ingredients.update(ingredient_list)
    print(distinct_ingredients)
    # Return the distinct ingredients as a list
    return list(distinct_ingredients)


# Call the function to execute
get_All_Ingredients()

def ingredientView(request):
    # Call the function to get distinct ingredients
    distinct_ingredients = get_All_Ingredients()
    return render(request, 'ingredient.html', {'distinct_ingredients': distinct_ingredients})




