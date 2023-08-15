from django.contrib import admin
from .models import *

admin.site.register(Recipe)
admin.site.register(IngredientsList)
admin.site.register(Result)
admin.site.register(Rating)

# Register your models here.
