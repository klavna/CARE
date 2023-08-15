from rest_framework.serializers import ModelSerializer
from .models import Recipe, IngredientsList, Result, Rating

class RecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

class IngredientSerializer(ModelSerializer):
    class Meta:
        model = IngredientsList
        fields = '__all__'
        
class ResultSerializer(ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
