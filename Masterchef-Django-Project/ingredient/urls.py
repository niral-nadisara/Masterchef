from django.urls import path
from ingredient import views

urlpatterns = [
    path("home/", views.ingredientView, name='home'),
    path("ingredients/", views.read_ingredient_by_name, name='read_ingredient_by_name'),

    path('contacts/', views.contactsView, name='contacts'),
    path('aboutus/', views.aboutUsView, name='aboutUs'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),

    path('save_recipe/', views.save_recipe, name='save_recipe'),
    path('recipes/saved/', views.saved_recipe, name='saved_recipe'),

]
