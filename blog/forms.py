from django import forms 
from .models import Comment

class CommentForm(forms.ModelForm):
    #user_name = forms.CharField(label="Nombre", max_length=120)
    #user_email = forms.EmailField(label="Correo")
    #comment = forms.CharField(label="Comentario",widget=forms.Textarea)
    
    class Meta:
        model = Comment
        #fields = "__all__"
        exclude = ["post"]
        labels = {
            "user_name": "Nombre",
            "user_email": "Correo",
            "comment": "Comentario",
        }