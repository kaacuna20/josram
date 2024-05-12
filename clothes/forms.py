from django import forms
from .models import Comment


class ClotheForm(forms.Form):

    
    def __init__(self, clothe, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Obtiene las tallas disponibles para la ropa dada
        colors_avaibles = clothe
        
        # Crea la tupla de opciones para ChoiceField
        choice_colors = []
        for color in colors_avaibles:
            tuple_color = (color.color_clothe.color, color.color_clothe.color)
            if tuple_color not in choice_colors:
                choice_colors.append(tuple_color)
       
       # Agrega el campo ChoiceField usando RadioSelect como widget
        self.fields['color'] = forms.ChoiceField(
            choices=choice_colors,
            widget=forms.RadioSelect,
            label="COLORES",
            initial=choice_colors[0][0]
        )

        # Obtener las tallas disponibles para el primer color por defecto
        choice_sizes = []
        for size_clothe in clothe:
            tuple_size = (size_clothe.size, size_clothe.size)
            if tuple_size not in choice_sizes:
                choice_sizes.append(tuple_size )
        

        # Agrega el campo ChoiceField usando RadioSelect como widget
        self.fields['size'] = forms.ChoiceField(
            choices=choice_sizes,
            widget=forms.RadioSelect,
            label="TALLAS", initial=choice_sizes[0][0]
        )

    cant = forms.IntegerField(label="CANTIDAD", min_value=1, initial=1)

     

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ["clothes"]
        labels = {
            "user_name": "Nombre",
            "user_email": "Correo",
            "comment": "Tu Opinión",
            "rating": "Tu calificación"
        }

class PriceForm(forms.Form):
    price_low = forms.IntegerField( min_value=0, initial=0, max_value=200000)
    price_hight = forms.IntegerField(min_value=0, max_value=200000)
    """def __init__(self, cant, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cant +=1
        self.fields['cant_product'] = forms.IntegerField(
            label="CANTIDAD", initial=cant
        )"""

    
    

#    user_name = forms.CharField(label="your name", max_length=100, error_messages={
#        "required": "your name must not be empty",
#        "max_length": "Please enter a shorter name!"
#    })