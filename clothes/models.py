from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Clothes(models.Model):
     GENDER_CHOICES = (
        ('hombres', 'Male'),
        ('mujeres', 'Female'),
     )
     TYPE_CHOICES = (
        ("crop top", 'crop top'),
        ('top deportivos', 'top deportivos'),
        ('sets', 'sets'),
        ('leggings', 'leggings'),
        ('enterizos', 'enterizos'),
        ('shorts', 'shorts'),
        ('pantalonetas', 'pantalonetas'),
        ('camisetas', 'camisetas'),
        ('hoodies', 'hoodies'),
        ('buzo', 'buzo'),
     )
     name = models.CharField(max_length=100, default="clothes")
     type = models.CharField(max_length=30, choices=TYPE_CHOICES)
     gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
     price = models.IntegerField()
     description = models.TextField(max_length=400, blank=True)
     slug = models.SlugField(default="", blank=True, null=False, db_index=True)
     slug_type = models.SlugField(default="", blank=True, null=False, db_index=True)
     date = models.DateField(auto_now=True)
     avg_rating = models.FloatField(null=True, blank=True)
     
     def __str__(self):
        return f"{self.name}"
     
     def __str__(self):
        return f" {self.get_type_display()}"


class ImageClothes(models.Model):
     color = models.CharField(max_length=20, default=None)
     main_image = models.ImageField(upload_to="clothes")
     model_image_1 = models.ImageField(upload_to="clothes", null=True)
     model_image_2 = models.ImageField(upload_to="clothes", null=True)
     other_image = models.ImageField(upload_to="clothes", null=True)
     clothes = models.ForeignKey(Clothes, related_name="Colors", on_delete=models.CASCADE, null=True)

     def __str__(self):
        return f" {self.color} - {self.clothes.name}"
     
     
class SizeClothes(models.Model):
     SIZE_CHOICES = (
        ('XS', 'XtraSmall'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
     )
     size = models.CharField(max_length=2, choices=SIZE_CHOICES)
     cant = models.IntegerField()
     color_clothe = models.ForeignKey(ImageClothes, related_name='sizes', on_delete=models.CASCADE, null=True)
     in_stock = models.BooleanField(default=True)
     
     def __str__(self):
        return f"{self.color_clothe.clothes} - {self.color_clothe} talla: {self.size}"
     
     def save(self, *args, **kwargs):
          if self.cant == 0:
               self.in_stock = False
               super().save(*args, **kwargs)
          else:
              self.in_stock = True
              super().save(*args, **kwargs)

class Comment(models.Model):
     RATING_CHOICE = (
    (0, '-'),
    (1, '⭐'),
    (2, '⭐⭐'),
    (3, '⭐⭐⭐'),
    (4, '⭐⭐⭐⭐'),
    (5, '⭐⭐⭐⭐⭐'),
     )
     user_name = models.CharField(max_length=120)
     user_email = models.EmailField()
     comment = models.TextField(max_length=400)
     date = models.DateField(auto_now=True)
     rating = models.IntegerField(default=0, choices=RATING_CHOICE)
     clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE, related_name="comments")

     def __str__(self):
        return f"{self.get_rating_display()}"
    

    
    