from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render  
from .forms import UserImage  
from .models import Ingredient, UploadImage  

from .models import Recipe

def index(request):
    recipes = Recipe.objects.all()
    context = {'recipes': recipes}
    return render(request, 'recipes/index.html', context)

def detail(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    # ingredients = recipe.ingredients.split(', ')
    context = {'recipe': recipe, 'ingredients': recipe.ingredient_set.all()}
    # context = {'recipe': recipe}
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
    if ("image" in data):
        image = UploadImage.objects.get(pk=data["image"])
        recipe = Recipe(
            recipe_name=data["recipe_name"],
            esstimated_duration_minutes=data["duration"],
            ingredients=", ".join(data["ingredients"].split("\n")),
            instructions=data["instructions"],
            image=image
        )
    else:
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

def edit_recipe(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    ingredients = recipe.ingredient_set.all()
    print(ingredients)
    if request.method == 'POST':
        print("HERE editing")
        form = UserImage(request.POST, request.FILES)
        form.save()
        img_object = form.instance
        return render(request, 'recipes/edit.html', {'recipe': recipe, 'form': form, 'img_obj': img_object, 'ingredients': ingredients})  
    form = UserImage()
    context = {'recipe': recipe, 'form': form, 'ingredients': ingredients}
    return render(request, 'recipes/edit.html', context)

def update_recipe(request, recipe_id):
    data = request.POST
    recipe = Recipe.objects.get(pk=recipe_id)
    recipe.recipe_name=data["recipe_name"]
    recipe.esstimated_duration_minutes=data["duration"]
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

    recipe.instructions=data["instructions"]
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