from django.db import models

# Create your models here.

class UploadImage(models.Model):  
    caption = models.CharField(max_length=200)  
    image = models.ImageField(upload_to='images')  
  
    def __str__(self):  
        return self.caption

class Recipe(models.Model):
    owner = models.ForeignKey('auth.User', related_name='recipes', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    duration = models.IntegerField('duration', default=0)
    instructions = models.TextField()
    image = models.ForeignKey(UploadImage, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def isFast(self):
        return self.duration <= 15

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text