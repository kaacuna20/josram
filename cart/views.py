from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from clothes.models import SizeClothes
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.http import JsonResponse
import secrets

# SDK de Mercado Pago
import mercadopago



class CartView(View):
    
    def get(self, request):
        stored_clothes = request.session.get("cart_clothes")
        is_enough = True
        context = {}
        len_cart = 0
        if request.session.get("cart_clothes") is not None:
            len_cart = len(request.session.get("cart_clothes"))

        if stored_clothes is None or len(stored_clothes) == 0:
            context["carts"] = []
            context["has_clothes"] = False
        else:
            cart = []
            for clothe in stored_clothes:
                is_stock_enough = True
                quantity = clothe["cant"]
                clothe_stored = SizeClothes.objects.get(pk=clothe["id"])
                if clothe_stored.cant < quantity or not clothe_stored.in_stock:
                    is_enough = False
                    is_stock_enough = False
                total_price = quantity * clothe_stored.color_clothe.clothes.price
                cart.append({
                    "size_pk": clothe_stored.pk,
                    "name": clothe_stored.color_clothe.clothes.name,
                    "slug": clothe_stored.color_clothe.clothes.slug,
                    "size": clothe_stored.size,
                    "color": clothe_stored.color_clothe.color,
                    "img": clothe_stored.color_clothe.main_image.url,
                    "price": clothe_stored.color_clothe.clothes.price,
                    "quantity": quantity,
                    "total_price": total_price,
                    "is_stock_enough": is_stock_enough
                })

            sum_prices = sum([item["total_price"] for item in cart])

            context["carts"] = cart
            context["has_clothes"] = True
            context["number"] = len_cart
            context["sum_prices"] = sum_prices
            context["is_enough"] = is_enough

        return render(request, "cart/my-cart.html", context)

    def post(self, request):
        stored_clothes = request.session.get("cart_clothes")
        if stored_clothes is None:
            stored_clothes = []

        scroll_pos = request.POST.get("scrollPos", "0")

        if "sizes_clothes_pk" in request.POST:
            sizes_clothes_id = int(request.POST["sizes_clothes_pk"])
            quantity = int(request.POST["sizes_clothes_cant"])
            stored_id = [item["id"] for item in stored_clothes]

            if sizes_clothes_id not in stored_id:
                slug_clothe = SizeClothes.objects.get(pk=sizes_clothes_id)
                clothe_choosed = {"id": sizes_clothes_id, "cant": quantity}
                stored_clothes.append(clothe_choosed)
                request.session["cart_clothes"] = stored_clothes
                name = SizeClothes.objects.get(pk=sizes_clothes_id).color_clothe.clothes.name
            elif sizes_clothes_id in stored_id:
                slug_clothe = SizeClothes.objects.get(pk=sizes_clothes_id)
                name = SizeClothes.objects.get(pk=sizes_clothes_id).color_clothe.clothes.name
                for item in stored_clothes:
                    if item["id"] == sizes_clothes_id:
                        item["cant"] = quantity
                request.session["cart_clothes"] = stored_clothes
            messages.success(request, f'Se agregó {name} al carrito!')
            return HttpResponseRedirect(f"/clothe/{slug_clothe.color_clothe.clothes.slug}?scrollPos={scroll_pos}")

        if "delete" in request.POST:
            clothe_to_delete_id = int(request.POST["sizes_pk"])
            clothe_to_delete_cant = int(request.POST["cant_product"])
            clothe_to_delete = {"id": clothe_to_delete_id, "cant": clothe_to_delete_cant}
            stored_clothes.remove(clothe_to_delete)
            request.session["cart_clothes"] = stored_clothes
            return HttpResponseRedirect(f"/cart?scrollPos={scroll_pos}")

        clothe_to_change_quantity = {"id": int(request.POST["sizes_pk"]), "cant": int(request.POST["cant_product"])}
        index = stored_clothes.index(clothe_to_change_quantity)

        if "plus" in request.POST:
            stored_clothes[index]["cant"] += 1
            request.session["cart_clothes"] = stored_clothes
            return HttpResponseRedirect(f"/cart?scrollPos={scroll_pos}")
        elif "minus" in request.POST:
            if stored_clothes[index]["cant"] > 1:
                stored_clothes[index]["cant"] -= 1
            request.session["cart_clothes"] = stored_clothes
        return HttpResponseRedirect(f"/cart?scrollPos={scroll_pos}")
        
        
class CheckOutView(View):

    def get(self, request):

        stored_clothes = request.session.get("cart_clothes")
        context = {}
        len_cart = len(request.session.get("cart_clothes"))
        cost_shipments = request.GET.get("cost_shipments")
        
        if cost_shipments is None:
            cost_shipments = 8000
        
        len_cart = 0
        if request.session.get("cart_clothes") is not None:
            len_cart = len(request.session.get("cart_clothes"))
        
        if  stored_clothes is None or len(stored_clothes)==0:
            context["carts"] = []
            context["has_clothes"] = False

        else:
            cart = []
            for clothe in stored_clothes:
                quantity = clothe["cant"]
                clothe_stored = SizeClothes.objects.get(pk=clothe["id"])
                total_price = quantity * clothe_stored.color_clothe.clothes.price
                cart.append({
                    "size_pk": clothe_stored.pk,
                    "name": clothe_stored.color_clothe.clothes.name,
                    "slug": clothe_stored.color_clothe.clothes.slug,
                    "size": clothe_stored.size,
                    "color": clothe_stored.color_clothe.color,
                    "img": clothe_stored.color_clothe.main_image.url,
                    "price": clothe_stored.color_clothe.clothes.price,
                    "quantity": quantity,
                    "total_price": total_price,
                    
                })

            sum_prices = sum([item["total_price"] for item in cart]) 
            
            context["carts"] = cart
            context["has_clothes"] = True
            context["number"] = len_cart
            context["sum_prices"] = sum_prices
            context["cost_shipments"] = cost_shipments
            context["order_josram"] = secrets.randbelow(10**12)
           
        return render(request, "cart/checkout.html", context)
    

    def post(self, request):

        stored_clothes = request.session.get("cart_clothes")

        if stored_clothes is None:
            stored_clothes = []
        
        if "sizes_clothes_pk" in request.POST:
            sizes_clothes_id = int(request.POST["sizes_clothes_pk"])
            quantity = int(request.POST["sizes_clothes_cant"])

            if len(stored_clothes) >= 1:
                # clean the cart
                stored_clothes.clear()

            clothe_choosed = {"id":sizes_clothes_id, "cant":quantity}
            # add the tuple in the list stored_clothe
            stored_clothes.append(clothe_choosed)
            # save it in the session
            request.session["cart_clothes"] = stored_clothes
        
        return HttpResponseRedirect("/cart/checkout")
    
class DirectPayment(View):
    @csrf_exempt
    def post(self, request, id_order):
        
        cost_shipments = int(request.POST.get("cost_shipments"))
        stored_clothes = request.session.get("cart_clothes")
        cart = []
        for clothe in stored_clothes:
            quantity = clothe["cant"]
            clothe_stored = SizeClothes.objects.get(pk=clothe["id"])
            total_price = quantity * clothe_stored.color_clothe.clothes.price

            cart.append({
                    "size_pk": clothe_stored.pk,
                    "name": clothe_stored.color_clothe.clothes.name,
                    "slug": clothe_stored.color_clothe.clothes.slug,
                    "size": clothe_stored.size,
                    "color": clothe_stored.color_clothe.color,
                    "img": clothe_stored.color_clothe.main_image.url,
                    "price": clothe_stored.color_clothe.clothes.price,
                    "quantity": quantity,
                    "total_price": total_price,
            })
        
        sum_prices = sum([item["total_price"] for item in cart]) + cost_shipments

        payer_data = {
                "name": request.POST.get("name"),
                "lastname": request.POST.get("lastname"),
                "email": request.POST.get("email"),
                "phone": request.POST.get("contact"),
                "address": request.POST.get("address")
            }
        
        merchand_order_josram = id_order

        return render(request, "cart/direct-payment-form.html",{
            "carts": cart,
            "payer": payer_data,
            "merchand_order": merchand_order_josram,
            "sum_prices": sum_prices,
            "cost_shipments": cost_shipments
        })


class ReferenceView(View):
    @csrf_exempt
    def post(self, request):
        # Get the id that are in the cart
        stored_clothes = request.session.get("cart_clothes")
        cart_mercadopago = []
        for clothe in stored_clothes:
                quantity = clothe["cant"]
                clothe_stored = SizeClothes.objects.get(pk=clothe["id"])
                cart_mercadopago.append({
                    "id": f"Item-ID-{clothe_stored.pk}",
                    "title": clothe_stored.color_clothe.clothes.name,
                    "description": f"Talla {clothe_stored.size} de color {clothe_stored.color_clothe.color}",
                    "unit_price": clothe_stored.color_clothe.clothes.price,
                    "currency_id": "COP",
                    "quantity": quantity,
                })

        expiration_date_from = datetime.now()
        expiration_date_to = expiration_date_from + timedelta(days=3)
      
        sdk = mercadopago.SDK("APP_USR-2915852037810033-052120-d6b889c55f57ff26fc0dfbdb6b38dc8e-1820373151")

        # Crea un ítem en la preferencia
        preference_data = {
            "auto_return": "approved",

            "items": cart_mercadopago,

            "installments": 1,
            "default_installments": 1,

            "payer": {
                "name": request.POST.get("name"),
                "surname": request.POST.get("lastname"),
                "email": request.POST.get("email"),
                "phone": {
                    "area_code": "57",
                    "number": request.POST.get("contact")
                },
                "address": {
                    "street_name": request.POST.get("address"),
                    
                    "zip_code": request.POST.get("zip_code")
                }
            },

            "receiver_address": {
			"zip_code": request.POST.get("zip_code"),
			"street_name": request.POST.get("address"),
			"apartment": request.POST.get("home"),
		},
            "back_urls": {
                "success": "https://9c04-190-84-119-237.ngrok-free.app/cart/success",
                "failure": "https://9c04-190-84-119-237.ngrok-free.app/cart/failure",
                "pending": "https://9c04-190-84-119-237.ngrok-free.app/cart/pending"
            },

             "excluded_payment_methods": [
                    { "id": "efecty" }
                ],
                "excluded_payment_types": [
                    { "id": "ticket" }
                ],
          
            
            "binary_mode": True,
            "shipments":{
            "cost": int(request.POST.get("cost_shipments")),
            "mode": "not_specified",
            },
            "statement_descriptor": "Compra en JOSRAM",
            "notification_url": f"https://9c04-190-84-119-237.ngrok-free.app/cart/notification",
         
            "expires": True,
            "expiration_date_from": f"{expiration_date_from.isoformat()}",
            "expiration_date_to": f"{expiration_date_to.isoformat()}"
        }
        
        preference_response = sdk.preference().create(preference_data)
        if preference_response.get("status") != 201:
            return JsonResponse(preference_response, status=preference_response.get("status", 400))
        preference = preference_response["response"]
    
        return HttpResponseRedirect(f"{preference['init_point']}")

def success(request):
    return render(request, "cart/success.html")

def failure(request):
    return render(request, "cart/failure.html")

def supend(request):
    return render(request, "cart/pending.html")

@csrf_exempt
@require_POST
def notificate(request):
    sdk = mercadopago.SDK("APP_USR-2915852037810033-052120-d6b889c55f57ff26fc0dfbdb6b38dc8e-1820373151")
    
    # Extract query parameters
    topic = request.GET.get("type")
    data_id = request.GET.get("data.id")

    if not topic or not data_id:
        print("Invalid request")
        return HttpResponse("Invalid request", status=200)

    merchant_order = None

    if topic == "payment":
        payment_response = sdk.payment().get(data_id)
        if payment_response["status"] != 200:
            print("Payment not found")
            return HttpResponse("Payment not found", status=200)
        
        payment = payment_response["response"]
        order_id = payment["order"]["id"]
        merchant_order_response = sdk.merchant_order().get(order_id)
        
        if merchant_order_response["status"] != 200:
            print("Merchant order not found")
            return HttpResponse("Merchant order not found", status=200)
        
        merchant_order = merchant_order_response["response"]
    
    elif topic == "merchant_order":
        merchant_order_response = sdk.merchant_order().get(data_id)
        
        if merchant_order_response["status"] != 200:
            print("Merchant order not found")
            return HttpResponse("Merchant order not found", status=200)
        
        merchant_order = merchant_order_response["response"]
       
    if not merchant_order:
        print("Merchant order not found")
        return HttpResponse("Merchant order not found", status=200)

    # Calculate paid amount
    paid_amount = sum(payment['transaction_amount'] for payment in merchant_order["payments"] if payment['status'] == 'approved')

    # Check if the total paid amount covers the order amount
    if paid_amount >= merchant_order["total_amount"]:
        if merchant_order.get("shipments") and merchant_order["shipments"][0]["status"] == "ready_to_ship":
            print("Totally paid. Print the label and release your item.")
            print(f"payment: {payment}" )
            print(f"merchant_order: {merchant_order}" )
            return HttpResponse("Totally paid. Print the label and release your item.", status=200)
        
        else:
            print("Totally paid. Release your item.")
            print(f"payment: {payment}" )
            print(f"merchant_order: {merchant_order}" )
            return HttpResponse("Totally paid. Release your item.", status=200)
    else:
        print("Not paid yet. Do not release your item.")
        print(f"payment: {payment}" )
        print(f"merchant_order: {merchant_order}" )
        return HttpResponse("Not paid yet. Do not release your item.", status=200)
    

#APK3K2C4S9JJJ548J9RXR7R3
#ACCOUNT SID = ACe90e72a4d8f44dfe6f0d04171fbd574f
# AUTH TOKEN  = 4b427536c3d3e8459492b6c099736060
#TWILIO NUMBER = +13374920319
"""
# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+13374920319',
                     to='+573003653344'
                 )

print(message.sid)
"""