from django import forms

class CheckOutForm(forms.Form):
    name = forms.CharField(label="Nombre", max_length=30, required=True)
    lastname = forms.CharField(label="Apellido", max_length=30, required=True)
    contact = forms.CharField(label="Contacto", max_length=10, required=True)
    email = forms.EmailField(label="Correo", required=True)
    address = forms.CharField(label="Dirección", max_length=30, required=True)
    departament = forms.CharField(label="Departamento", max_length=30, required=True)
    city = forms.CharField(label="Ciudad", max_length=30, required=True)
    zip_code = forms.CharField(label="Código postal", max_length=30, required=False)
