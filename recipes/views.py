from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render  
from .forms import UserImage  
from .models import UploadImage  

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
    if request.method == 'POST':
        print("HERE editing")
        form = UserImage(request.POST, request.FILES)
        form.save()
        img_object = form.instance
        return render(request, 'recipes/edit.html', {'recipe': recipe, 'form': form, 'img_obj': img_object})  
    form = UserImage()
    context = {'recipe': recipe, 'form': form}
    return render(request, 'recipes/edit.html', context)

def update_recipe(request, recipe_id):
    data = request.POST
    recipe = Recipe.objects.get(pk=recipe_id)
    recipe.recipe_name=data["recipe_name"]
    recipe.esstimated_duration_minutes=data["duration"]
    recipe.ingredients=", ".join(data["ingredients"].split("\n"))
    recipe.instructions=data["instructions"]
    if data["image"]:
        image = UploadImage.objects.get(pk=data["image"])
        recipe.image=image
    recipe.save()
    return HttpResponseRedirect("/recipes")

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