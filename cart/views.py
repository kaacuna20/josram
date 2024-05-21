from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from clothes.models import SizeClothes
from django.contrib import messages
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import datetime
# SDK de Mercado Pago
import mercadopago
# Agrega credenciales

# Create your views here.


class CartView(View):

    def get(self, request):
        stored_clothes = request.session.get("cart_clothes")
        context = {}
        len_cart = 0
        if request.session.get("cart_clothes") is not None:
            len_cart = len(request.session.get("cart_clothes"))
        
        if  stored_clothes is None or len(stored_clothes)==0:
            context["carts"] = []
            context["has_clothes"] = False
        else:
            stored_id = [item["id"] for item in stored_clothes]
            stored_cant = [item["cant"] for item in stored_clothes] 
            clothes = SizeClothes.objects.filter(id__in=stored_id)
            index = 0
            cart = []
            for clothe in clothes:
                quantity = stored_cant[index]
                total_price = quantity*clothe.color_clothe.clothes.price
                cart.append({
                "size_pk": clothe.pk,
                "name": clothe.color_clothe.clothes.name,
                "slug": clothe.color_clothe.clothes.slug,
                "size": clothe.size,
                "color": clothe.color_clothe.color,
                "img": clothe.color_clothe.main_image.url,
                "price": clothe.color_clothe.clothes.price,
                "quantity": quantity,
                "total_price": total_price
                })
                index += 1
            
            sum_prices = sum([item["total_price"] for item in cart])
            
            context["carts"] = cart
            context["has_clothes"] = True
            context["number"] = len_cart
            context["sum_prices"] = sum_prices
           
        return render(request, "cart/my-cart.html", context)

    def post(self, request):

        stored_clothes = request.session.get("cart_clothes")

        if stored_clothes is None:
            stored_clothes = []
        
        if "sizes_clothes_pk" in request.POST:
            sizes_clothes_id = int(request.POST["sizes_clothes_pk"])
            quantity = int(request.POST["sizes_clothes_cant"])

            #extract all 'id' and quantity from the list stored_clothes for separated
            stored_id = [item["id"] for item in stored_clothes]

            # verify if the id of size clothe is not in the session to add it
            if sizes_clothes_id not in stored_id:
                # get the slug to redirect to 'clothe-details' route
                slug_clothe = SizeClothes.objects.get(pk=sizes_clothes_id)
                clothe_choosed = {"id":sizes_clothes_id, "cant":quantity}
                # add the tuple in the list stored_clothe
                stored_clothes.append(clothe_choosed)
                # save it in the session
                request.session["cart_clothes"] = stored_clothes
                name = SizeClothes.objects.get(pk=sizes_clothes_id).color_clothe.clothes.name

            # if the 'id' of size clothe is in the session, change the quantity 
            elif sizes_clothes_id in stored_id:
                slug_clothe = SizeClothes.objects.get(pk=sizes_clothes_id)
                name = SizeClothes.objects.get(pk=sizes_clothes_id).color_clothe.clothes.name
                for item in stored_clothes:
                    if item["id"] == sizes_clothes_id:
                        item["cant"] = quantity
                # save it in the session
                request.session["cart_clothes"] = stored_clothes
            # send a pop alerting that the clothe is saved in the cart
            messages.success(request, f'Se agregó {name} al carrito!')
                
            return HttpResponseRedirect("/clothe/" + slug_clothe.color_clothe.clothes.slug)

        if "sizes_pk" in request.POST:
            print(stored_clothes)
            # delete a clothe in the cart
            clothe_to_delete = {"id":int(request.POST["sizes_pk"]), "cant":int(request.POST["sizes_cant"])}
            stored_clothes.remove(clothe_to_delete)
            request.session["cart_clothes"] = stored_clothes
            return HttpResponseRedirect("/cart")
        
       
        

class CheckOutView(View):
    def get(self, request):

        stored_clothes = request.session.get("cart_clothes")
        context = {}
        len_cart = len(request.session.get("cart_clothes"))
        
        len_cart = 0
        if request.session.get("cart_clothes") is not None:
            len_cart = len(request.session.get("cart_clothes"))
        
        if  stored_clothes is None or len(stored_clothes)==0:
            context["carts"] = []
            context["has_clothes"] = False

        else:
            stored_id = [item["id"] for item in stored_clothes]
            stored_cant = [item["cant"] for item in stored_clothes] 
            clothes = SizeClothes.objects.filter(id__in=stored_id)
            index = 0
            cart = []
            for clothe in clothes:
                quantity = stored_cant[index]
                total_price = quantity*clothe.color_clothe.clothes.price
                cart.append({
                "size_pk": clothe.pk,
                "name": clothe.color_clothe.clothes.name,
                "slug": clothe.color_clothe.clothes.slug,
                "size": clothe.size,
                "color": clothe.color_clothe.color,
                "img": clothe.color_clothe.main_image.url,
                "price": clothe.color_clothe.clothes.price,
                "quantity": quantity,
                "total_price": total_price
                })
                index += 1
            
            sum_prices = sum([item["total_price"] for item in cart])
            
            context["carts"] = cart
            context["has_clothes"] = True
            context["number"] = len_cart
            context["sum_prices"] = sum_prices
           
        return render(request, "cart/checkout.html", context)

    def post(self, request):

        stored_clothes = request.session.get("cart_clothes")

        if stored_clothes is None:
            stored_clothes = []
        
        if "sizes_clothes_pk" in request.POST:
            sizes_clothes_id = int(request.POST["sizes_clothes_pk"])
            quantity = int(request.POST["sizes_clothes_cant"])

            if len(stored_clothes) == 0:
                clothe_choosed = {"id":sizes_clothes_id, "cant":quantity}
                # add the tuple in the list stored_clothe
                stored_clothes.append(clothe_choosed)
                # save it in the session
                request.session["cart_clothes"] = stored_clothes

            elif len(stored_clothes) >= 1:
                stored_clothes.clear()
                clothe_choosed = {"id":sizes_clothes_id, "cant":quantity}
                # add the tuple in the list stored_clothe
                stored_clothes.append(clothe_choosed)
                # save it in the session
                request.session["cart_clothes"] = stored_clothes

        return HttpResponseRedirect("/cart/checkout")


def payment(request):
    """URL="https://api.mercadopago.com/v1/payment_methods"
    params = {"public_key": "TEST-971dffb2-2411-415d-9981-ded0246e2de0"}
    response = requests.get(url=URL, params=params)
    json_response = response.json()
    for i in json_response:
        if i["id"] == "pse":
            print(i["financial_institutions"])"""
    
    now = datetime.now()
    print(now)
    sdk = mercadopago.SDK("TEST-2915852037810033-052022-9ee7aa74c0d6e65734a6f807b28ad266-1820373151")

    # Cria um item na preferência
    # Crea un ítem en la preferencia
    preference_data = {

      
        "auto_return": "approved",

        "items": [
            {
                "id": "item-ID-1234",
                "title": "Meu produto",
                "currency_id": "BRL",
                "picture_url": "https://www.mercadopago.com/org-img/MP3/home/logomp3.gif",
                "description": "Descrição do Item",
                "category_id": "art",
                "quantity": 1,
                "unit_price": 75
            },
            {
            "title": "Mi producto2",
            "quantity": 2,
            "unit_price": 96
        }
        ],

        
        "installments": 5,
        "default_installments": 1,


        "payer": {
            "name": "João",
            "surname": "Silva",
            "email": "user@email.com",
            "phone": {
                "area_code": "11",
                "number": "4444-4444"
            },
            "identification": {
                "type": "CPF",
                "number": "19119119100"
            },
            "address": {
                "street_name": "Street",
                "street_number": 123,
                "zip_code": "06233200"
            }
        },
        "back_urls": {
            "success": "https://d672-2800-e2-2a80-32b-29cf-b5a2-7691-f7d.ngrok-free.app/cart/success",
            "failure": "https://d672-2800-e2-2a80-32b-29cf-b5a2-7691-f7d.ngrok-free.app/cart/failure",
            "pending": "https://d672-2800-e2-2a80-32b-29cf-b5a2-7691-f7d.ngrok-free.app/cart/pending"
        },
        

        "shipments":{
        "cost": 1000,
        "mode": "not_specified",
        },
       
        "notification_url": "https://d672-2800-e2-2a80-32b-29cf-b5a2-7691-f7d.ngrok-free.app/cart/notificate",
        "statement_descriptor": "MEUNEGOCIO",
        "external_reference": "Reference_1234",
        "expires": True,
        "expiration_date_from": "2024-05-20T12:00:00.000-04:00",
        "expiration_date_to": "2024-05-23T12:00:00.000-04:00"
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    print(preference["init_point"])
    

    return render(request, "cart/form-payment.html", {
        "preference": preference
    })

def success(request):
    return HttpResponse("<h1>transacion exitosa</h1>")

def failure(request):
    return HttpResponse("<h1>transacion fallida</h1>")

def supend(request):
    return HttpResponse("<h1>transacion suspendida</h1>")

@csrf_exempt
def notificate(request):
    if request.method == "POST":
        print("notificar")
        return HttpResponse("<h1>Notificar</h1>")