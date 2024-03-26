from django.contrib import admin
from .models import ChefRecipe

# Register your models here.
class ChefRecipeAdmin(admin.ModelAdmin):
    list_display=('id','cuisine','time','steps','description','ingredients')
    search_fields=('time','ingredients')
admin.site.register(ChefRecipe,ChefRecipeAdmin)