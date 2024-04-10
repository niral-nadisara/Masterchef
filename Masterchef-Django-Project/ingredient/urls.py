from django.urls import path
from ingredient import views

urlpatterns = [
    path("home/", views.ingredientView, name='home'),
    path("ingredients/", views.read_ingredient_by_name, name='read_ingredient_by_name'),
    path('search/<int:ingredientId>/', views.searchView),

    #api
    path('api/ingredient_id/<ingredientName>', views.get_ingredientId),
    path('api/match_recipe/', views.get_match_recipe),
]
