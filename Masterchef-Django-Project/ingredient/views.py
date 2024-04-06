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


# def read_ingredient_by_name(request):
#     #all_recipe_ingredients = []
#     #print("This is the empty array of all ingredients", all_recipe_ingredients)
#     data = ChefRecipe.objects.all()
    
#     if 'q' in request.GET:
#         q = request.GET['q']
#         print(q) # Debug purpose
#         query_terms = q.split(",")
#         print(query_terms) # Debug purpose

#         for term in query_terms:
#             data = data.filter(ingredients__icontains=term)
            
#             data_ingredients = data.first().ingredients
#             data_cuisine = data.first().cuisine
#             data_time = data.first().time

#             #print(data) #Debug purpose
#             #print("This are the ingredients: ", data_ingredients) # Debug purpose
#             #print("This is the cuisine: ", data_cuisine) # Debug purpose
#             #print("This is the time taken to prepare: ", data_time) # Debug purpose
            
#     # Convert queryset data to a list of dictionaries
#     data_dict_list = []
#     for instance in data:
#         instance_dict = {
#             'cuisine': instance.cuisine,
#             'time': instance.time,
#             'ingredients': instance.ingredients,
#             'steps': instance.steps
#             # Add other fields as needed
#         }
#         data_dict_list.append(instance_dict)

#     # Take only the first 10 items for the first page
#     first_page_data = data_dict_list[:10]
#     print(first_page_data)

#     #print("Data as Dictionary:", data_dict_list)
#     # Convert the list of dictionaries to JSON format
#     json_data = json.dumps(data_dict_list, indent=4)  # Indent for pretty printing

#     # Print the JSON formatted data
#     #print("Data as JSON:", json_data)

#     paginator = Paginator(data, 10)
#     page_number = request.GET.get('page', 1)
#     data = paginator.get_page(page_number)

#     return render(request, 'ingredient.html', {'data': data})

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
        instance_dict = {
            'cuisine': instance.cuisine,
            'time': instance.time,
            'ingredients': instance.ingredients,
            'steps': instance.steps,
            'description': instance.description
            # Add other fields as needed
        }
        data_dict_list.append(instance_dict)

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