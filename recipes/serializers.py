from rest_framework import serializers
from recipes.models import Recipe, Ingredient, Instruction
from django.contrib.auth.models import User


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']

class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ['text']

class RecipeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    ingredient_set = IngredientSerializer(many=True, required=False)
    instruction_set = InstructionSerializer(many=True, required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'owner', 'name', 'duration', 'instruction_set', 'ingredient_set', 'image']

    def create(self, validated_data):
        print('validated data: ', validated_data)
        ingredients = validated_data.pop('ingredient_set')
        instructions = validated_data.pop('instruction_set')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            Ingredient.objects.create(recipe=recipe, **ingredient)
        for instruction in instructions:
            Instruction.objects.create(recipe=recipe, **instruction)
        return recipe

class UserSerializer(serializers.ModelSerializer):
    recipes = serializers.HyperlinkedRelatedField(many=True, view_name='recipe-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'recipes']
