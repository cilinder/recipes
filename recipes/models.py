from django.db import models

# Create your models here.

class UploadImage(models.Model):  
    caption = models.CharField(max_length=200)  
    image = models.ImageField(upload_to='images')  
  
    def __str__(self):  
        return self.caption

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=100)
    esstimated_duration_minutes = models.IntegerField('duration', default=0)
    # ingredients = models.ForeignKey
    # ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ForeignKey(UploadImage, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.recipe_name

    def isFast(self):
        return self.esstimated_duration_minutes <= 15

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"