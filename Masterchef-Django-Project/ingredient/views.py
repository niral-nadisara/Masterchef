from audioop import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ingredientItem, recipeItem, ChefRecipe, categories, SavedRecipe
import json
from django.core.serializers import serialize
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm, SignUpForm


#View for Saving Recipes
@login_required
def save_recipe(request):
    if request.method == 'POST' and 'recipe_id' in request.POST:
        recipe_id = request.POST['recipe_id']
        user = request.user

        # Check if the recipe is already saved by the user
        if SavedRecipe.objects.filter(user=user, recipe_id=recipe_id).exists():
            return JsonResponse({'message': 'Recipe already saved'})

        # Save the recipe for the user
        saved_recipe = SavedRecipe(user=user, recipe_id=recipe_id)
        saved_recipe.save()

        return JsonResponse({'message': 'Recipe saved successfully'})

    return JsonResponse({'error': 'Invalid request'})

#View for login page
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after successful login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

#View for logout
def logout_view(request):
    logout(request)
    return redirect('login')

#View for Sign Up
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password == confirm_password:
                user = User.objects.create_user(username, email, password)
                user.save()
                messages.success(request, 'Account created successfully!')
                return redirect('login')  # Redirect to login page after successful signup
            else:
                messages.error(request, 'Passwords do not match.')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


#View for Contacts Page
def contactsView(request):
    return render(request, 'contacts.html')

#View for About Us Page
def aboutUsView(request):
    return render(request, 'aboutUs.html')

#view for Saved Recipes page
def saved_recipe(request):
    
    # Fetch saved recipes for the current user
    saved_recipes = SavedRecipe.objects.filter(user_id=request.user)

    print("Saved Recipes:", saved_recipes)
    
    context = {
        'saved_recipes': saved_recipes,

    }
    return render(request, 'savedRecipes.html', context)

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

@login_required
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
            'id': instance.id,
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

# def ingredientView(request):
#     # Call the function to get distinct ingredients
#     distinct_ingredients = get_All_Ingredients()
#     return render(request, 'ingredient.html', {'distinct_ingredients': distinct_ingredients})

def get_All_Ingredients(column_name):

    # Retrieve distinct ingredients from the specified column of the ChefRecipe model
    data = categories.objects.values_list(column_name, flat=True) #[:10]

    #print("Ingredients:", data) # Debug purposes

    # Initialize a set to store distinct ingredients
    distinct_ingredients = set()

    # Iterate over the ingredients in the first 10 records
    for ingredients in data:
        # Check if ingredients is not None
        if ingredients:
            # Split the ingredients string into a list
            ingredient_list = ingredients.split(',')
            # Add each ingredient to the set of distinct ingredients
            distinct_ingredients.update(ingredient_list)

    # Return the distinct ingredients as a list
    return list(distinct_ingredients)


def ingredientView(request):
    # Call the function to get distinct ingredients for a specific column
    distinct_vegetables = get_All_Ingredients('vegetables')
    distinct_fruits = get_All_Ingredients('Fruits')
    distinct_proteins = get_All_Ingredients('proteins')
    distinct_grainsnflours = get_All_Ingredients('grains_and_flours')
    distinct_nutsnseeds = get_All_Ingredients('nuts_and_seeds')
    distinct_sweeteners = get_All_Ingredients('sweeteners')
    distinct_dairy_and_egg_products = get_All_Ingredients('dairy_and_egg_products')
    distinct_condiments_and_sauces = get_All_Ingredients('condiments_and_sauces')
    distinct_herbs_spices_and_seasonings = get_All_Ingredients('herbs_spices_and_seasonings')
    return render(request, 'ingredient.html', {'distinct_vegetables': distinct_vegetables,'distinct_fruits': distinct_fruits, 'distinct_proteins': distinct_proteins,
                                               'distinct_grainsnflours': distinct_grainsnflours, 'distinct_nutsnseeds': distinct_nutsnseeds, 'distinct_sweeteners': distinct_sweeteners,
                                               'distinct_dairy_and_egg_products': distinct_dairy_and_egg_products, 'distinct_condiments_and_sauces': distinct_condiments_and_sauces,
                                               'distinct_herbs_spices_and_seasonings': distinct_herbs_spices_and_seasonings})




