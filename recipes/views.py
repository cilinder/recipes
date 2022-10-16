from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Recipe

def index(request):
    recipes = Recipe.objects.all()
    context = {'recipes': recipes}
    return render(request, 'recipes/index.html', context)

def detail(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    ingredients = recipe.ingredients.split(', ')
    context = {'recipe': recipe, 'ingredients': ingredients}
    return render(request, 'recipes/detail.html', context)

def new_recipe(request):
    return render(request, 'recipes/new_recipe.html')

def save_recipe(request):
    data = request.POST
    recipe = Recipe(
        recipe_name=data["recipe_name"],
        esstimated_duration_minutes=data["duration"],
        ingredients=", ".join(data["ingredients"].split("\n")),
        instructions=data["instructions"],
    )
    recipe.save()
    return HttpResponseRedirect("/recipes")

def delete_recipe(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    recipe.delete()
    # return render(request, 'recipes/index.html', {'recipes': Recipe.objects.all()})
    return HttpResponseRedirect("/recipes")