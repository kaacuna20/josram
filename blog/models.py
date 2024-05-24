from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=200)
    image = models.ImageField(upload_to="post", null=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True)#, db_index=True) => unique=True implies an index
    content = models.TextField(validators=[MinLengthValidator(10)])

    def __str__(self):
        return f"{self.title} "
    
class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    comment = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")