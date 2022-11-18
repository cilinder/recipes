from rest_framework import serializers
from recipes.models import Recipe, Ingredient
from django.contrib.auth.models import User


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']

class RecipeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    ingredient_set = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ['owner', 'name', 'duration', 'instructions', 'ingredient_set']

class UserSerializer(serializers.ModelSerializer):
    recipes = serializers.HyperlinkedRelatedField(many=True, view_name='recipe-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'recipes']
