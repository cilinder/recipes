from django.db import models

# Create your models here.

class Recipe(models.Model):
  recipe_name = models.CharField(max_length=100)
  esstimated_duration_minutes = models.IntegerField('duration', default=0)
  ingredients = models.TextField()
  instructions = models.TextField()
  
  def __str__(self):
    return self.recipe_name

  def isFast(self):
    return self.esstimated_duration_minutes <= 15