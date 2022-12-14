from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render  
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import JSONParser, FileUploadParser

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from recipes.permissions import IsOwnerOrReadOnly
from .forms import UserImage  
from .models import Ingredient, UploadImage, Recipe, Instruction
from .serializers import RecipeSerializer, UserSerializer
from .authentications import BearerAuthentication

import json

def index(request):
    recipes = Recipe.objects.all()
    context = {'recipes': recipes}
    return render(request, 'recipes/index.html', context)

def detail(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    context = {'recipe': recipe, 'ingredients': recipe.ingredient_set.all(), 'instructions': recipe.instruction_set.all()}
    return render(request, 'recipes/detail.html', context)

def new_recipe(request):
    if request.method == 'POST':
        form = UserImage(request.POST, request.FILES)
        form.save()
        img_object = form.instance    
        return render(request, 'recipes/new_recipe.html', {'form': form, 'img_obj': img_object})  
    else:
        form = UserImage()
        return render(request, 'recipes/new_recipe.html', {'form': form})

def save_recipe(request):
    data = request.POST
    user = User.objects.get(pk=1)
    if ("image" in data):
        image = UploadImage.objects.get(pk=data["image"])
        recipe = Recipe(
            owner=user,
            name=data["name"],
            duration=data["duration"],
            image=image,
        )
    else:
        recipe = Recipe(
            owner=user,
            name=data["name"],
            duration=data["duration"],
        )
    recipe.save()
    for i in range(1,6):
        if f"name_new_{i}" in data:
            print(data[f"name_new_{i}"])
        if f"name_new_{i}" in data and len(data[f"name_new_{i}"]) > 0:
            new_ingredient = Ingredient(name=data[f"name_new_{i}"], quantity=data[f"quantity_new_{i}"], unit=data[f"unit_new_{i}"], recipe=recipe)
            new_ingredient.save()
    for line in data["instructions"].split("\n"):
        instruction = Instruction(recipe=recipe, text=line)
        instruction.save()
    return HttpResponseRedirect("/recipes")

def delete_recipe(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    recipe.delete()
    return HttpResponseRedirect("/recipes")

def edit_recipe(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    ingredients = recipe.ingredient_set.all()
    instructions = ", ".join(list(recipe.instruction_set.all()))
    if request.method == 'POST':
        print("HERE editing")
        form = UserImage(request.POST, request.FILES)
        form.save()
        img_object = form.instance
        return render(request, 'recipes/edit.html', {'recipe': recipe, 'form': form, 'img_obj': img_object, 'ingredients': ingredients, 'instructions': instructions})  
    form = UserImage()
    context = {'recipe': recipe, 'form': form, 'ingredients': ingredients, 'instructions': instructions}
    return render(request, 'recipes/edit.html', context)

def update_recipe(request, recipe_id):
    data = request.POST
    recipe = Recipe.objects.get(pk=recipe_id)
    recipe.name=data["name"]
    recipe.duration=data["duration"]
    # ingredients = recipe.ingredient_set.all()
    print(data.keys())
    ingredient_ids = [k.split("_")[-1] for k in data if "ing_name" in k]
    for ing_id in ingredient_ids:
        ing_name = data[f"ing_name_{ing_id}"]
        ing_qty = data[f"ing_qty_{ing_id}"]
        ing_unit = data[f"ing_unit_{ing_id}"]
        try:
            ingredient = Ingredient.objects.get(pk=ing_id)
            ingredient.name = ing_name
            ingredient.quantity = ing_qty
            ingredient.unit = ing_unit
        except:
            ingredient = Ingredient(name=ing_name, quantity=ing_qty, unit = ing_unit, recipe=recipe)
        ingredient.save()

    if "name_new" in data and len(data["name_new"]) > 0:
        new_ingredient = Ingredient(name=data["name_new"], quantity=data["qty_new"], unit=data["unit_new"], recipe=recipe)
        print("Saving new ingredient")
        new_ingredient.save()

    for line in data["instructions"].split("\n"):
        instruction = Instruction(recipe=recipe, text=line)
        instruction.save()
    if "image" in data:
        image = UploadImage.objects.get(pk=data["image"])
        recipe.image=image
    recipe.save()
    return HttpResponseRedirect(f"/recipes/{recipe.id}")

def image_request(request):  
    if request.method == 'POST':  
        form = UserImage(request.POST, request.FILES)  
        if form.is_valid():  
            form.save()
            # Getting the current instance object to display in the template  
            img_object = form.instance  
              
            return render(request, 'recipes/image_form.html', {'form': form, 'img_obj': img_object})  
    else:
        form = UserImage()  
  
    return render(request, 'recipes/image_form.html', {'form': form})

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'recipes': reverse('recipe-list', request=request, format=format),
    })

class RecipeList(APIView):
    """
    List all recipes, or create a new snippet.
    """
    # authentication_classes = [BearerAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    def get(self, request, *args, **kwargs):
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        ingredients = json.loads(request.data["ingredient_set"])
        instructions = json.loads(request.data["instruction_set"])
        data = request.data
        if 'image' in data:
            recipe_serializer = RecipeSerializer(data={
                'name': data['name'] ,
                'duration': data['duration'],
                'instruction_set': instructions,
                'ingredient_set': ingredients,
                'image': data['image'],
            })
        else:
            recipe_serializer = RecipeSerializer(data={
                'name': data['name'] ,
                'duration': data['duration'],
                'instruction_set': instructions,
                'ingredient_set': ingredients,
            })
        if recipe_serializer.is_valid():
            user = User.objects.get(pk=1)
            recipe_serializer.save(owner=user)
            return Response(recipe_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', recipe_serializer.errors)
            return Response(recipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
