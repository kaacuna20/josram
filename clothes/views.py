from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .models import Clothes, ImageClothes, SizeClothes, Comment
from .forms import ClotheForm, CommentForm, PriceForm
from django.urls import reverse
from django.http import JsonResponse
import json
# Create your views here.




class StartPageView(ListView):
    template_name = "clothes/index.html"
    model = ImageClothes
    context_object_name = "clothes"

    def get_queryset(self):
        querySet = super().get_queryset()
        data = querySet[:4]
        return data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["number"] = len(self.request.session.get("cart_clothes"))
        return context

class AllProducts(View):

    def get(self, request):
        all_products = ImageClothes.objects.all()
        context = {
            "clothes": all_products,
            "clothes_number": all_products.count(),
            "number": len(self.request.session.get("cart_clothes")),
            "colors": ImageClothes.objects.values("color").distinct,
            "price_form": PriceForm()
        }
        return render(request, "clothes/all-products.html", context)
    
    def post(self, request):
        filter_session = request.session.get("filters")

        if filter_session is None:
            filter_session = []
       

        if "color_filter" in request.POST:
            color_filter = request.POST["color_filter"]
            filter_colors = ImageClothes.objects.filter(color=color_filter)
            filter_session.append(color_filter)
            #ImageClothes.objects.filter(clothes__price__range=(0, 30000))
            

        if "filter_price" in request.POST:
            min_price = int(request.POST["price_low"])
            max_price =int(request.POST["price_hight"])
            #filter_price = ImageClothes.objects.filter(clothes__price__range=(min_price, max_price))

        """try:
            
            filter_product = filter_colors.intersection(filter_price)
        except UnboundLocalError:
            print("nointercep")
            try:
                print("nointercep1")
                filter_product = filter_price
            except UnboundLocalError:
                filter_product = filter_colors"""
        print(filter_session)
        context = {
            "clothes": filter_colors,
            "clothes_number": filter_colors.count(),
            "number": len(self.request.session.get("cart_clothes")),
            "colors": ImageClothes.objects.values("color").distinct,
            "price_form": PriceForm(request.POST)
            }

        return render(request, "clothes/all-products.html", context)

        
   

def show_clothes_by_type(request, slug_type):
    type_clothes = ImageClothes.objects.filter(clothes__slug_type=slug_type)
   
    dict_type = {
        'crop-top': 'crop top',
        'top-deportivos': 'top deportivos',
        'sets': 'sets',
        'leggings': 'leggings',
        'enterizos': 'enterizos',
        'shorts': 'shorts',
        'pantalonetas': 'pantalonetas',
        'camisetas': 'camisetas',
        'hoodies': 'hoodies',
        'buzo': 'buzo',
    }
    
    if request.method == "POST":
        if "color_filter" in request.POST:
            color_filter = request.POST["color_filter"]
            filter_product = ImageClothes.objects.filter(color=color_filter, clothes__slug_type=slug_type)

            context = {
            "clothes": filter_product,
            "clothes_number": filter_product.count(),
            "number": len(request.session.get("cart_clothes")),
            "colors": ImageClothes.objects.values("color").distinct
        }
        return render(request, "clothes/all-products.html", context)
    
    
    return render(request, "clothes/type-clothes.html", {
        "clothes": type_clothes,
        "clothes_number": type_clothes.count(),
        "type": dict_type[slug_type],
        "number": len(request.session.get("cart_clothes")),
        "colors": ImageClothes.objects.values("color").distinct
    })


def show_clothes_by_gender(request, gender):
    gender_clothes = ImageClothes.objects.filter(clothes__gender=gender)
    
    if request.method == "POST":
        if "color_filter" in request.POST:
            color_filter = request.POST["color_filter"]
            filter_product = ImageClothes.objects.filter(color=color_filter, clothes__gender=gender)

            context = {
            "clothes": filter_product,
            "clothes_number": filter_product.count(),
            "number": len(request.session.get("cart_clothes")),
            "colors": ImageClothes.objects.values("color").distinct
        }
        return render(request, "clothes/all-products.html", context)


    dict_gender = {
        "hombres": "Hombres",
        "mujeres": "Mujeres",
    }

    return render(request, "clothes/gender-clothes.html", {
        "clothes": gender_clothes,
        "clothes_number": gender_clothes.count(),
        "gender": dict_gender[gender],
        "number": len(request.session.get("cart_clothes")),
        "colors": ImageClothes.objects.values("color").distinct
    })


def clothe_details(request, slug):
    # name of clothe
    clothe_select = Clothes.objects.get(slug=slug)
    # colors asociated to that clothe
    color_clothes = ImageClothes.objects.filter(clothes__slug=slug)
    # sizes asociated to that clothe inside the form
    size_clothes_form = SizeClothes.objects.filter(color_clothe__clothes__slug=slug)
    #forms
    comment_form = CommentForm()
    form = ClotheForm(size_clothes_form)
    added_cart = True
    default_size = form.fields["size"].initial
    default_color = form.fields["color"].initial
    size_clothes = SizeClothes.objects.get(color_clothe__clothes__slug=slug, color_clothe__color=default_color, size=default_size)
    is_enough = True
    
    if int(form.fields["cant"].initial) > size_clothes.cant:
        is_enough = False
    
    if request.method == 'POST':
       
        if "verify" in request.POST:
            form = ClotheForm(size_clothes_form, request.POST)
            if form.is_valid():
                post_color = request.POST["color"]
                post_size = request.POST["size"]
                sizes_clothes = SizeClothes.objects.get(color_clothe__clothes__slug=slug, color_clothe__color=post_color, size=post_size )
                
                if int(request.POST["cant"]) > sizes_clothes.cant:
                    is_enough = False
                context = {
                    "color_clothes": color_clothes,
                    "clothe_details": clothe_select,
                    "form": form,
                    "is_enough": is_enough,
                    "comment_form": comment_form,
                    "comments": clothe_select.comments.all().order_by("-date"),
                    "size_clothes": sizes_clothes,
                    "number": len(request.session.get("cart_clothes")),
                    "added_cart": added_cart
                }
                    
                return render(request, "clothes/clothes-details.html", context)
       
            
                #return redirect("sales-cart")
            #return HttpResponseRedirect("/sales-cart")
             
        #clothe_select = SizeClothes.objects.get(color_clothe__clothes__slug='esqueleto-vibes', color_clothe__color='purpura', size='S').cant 
        elif "comment" in request.POST:
            comment_form = CommentForm(request.POST)
            clothe_select = Clothes.objects.get(slug=slug)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.clothes = clothe_select
                comment.save()
                return HttpResponseRedirect(reverse("clothes-details", args=[slug]))
            else:
                print(comment_form.errors)
            #return redirect("clothes-details", color=color, slug=slug)
        
    context = {
            "color_clothes": color_clothes,
            "clothe_details": clothe_select,
            "form": form,
            "is_enough": is_enough,
            "comment_form": comment_form,
            "comments": clothe_select.comments.all().order_by("-date"),
            "size_clothes": size_clothes,
            "number": len(request.session.get("cart_clothes")),
            "added_cart": added_cart
        }
    return render(request, "clothes/clothes-details.html", context)
    


class CartView(View):

    def get(self, request):
        stored_clothes = request.session.get("cart_clothes")
        context = {}
        print(stored_clothes)
        
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
            context["number"] = len(request.session.get("cart_clothes"))
            context["sum_prices"] = sum_prices
           
        return render(request, "clothes/cart.html", context)

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

            # if the 'id' of size clothe is in the session, change the quantity 
            elif sizes_clothes_id in stored_id:
                slug_clothe = SizeClothes.objects.get(pk=sizes_clothes_id)
                for item in stored_clothes:
                    if item["id"] == sizes_clothes_id:
                        item["cant"] = quantity
                # save it in the session
                request.session["cart_clothes"] = stored_clothes
                
            return HttpResponseRedirect("/clothe/" + slug_clothe.color_clothe.clothes.slug)

        """clothes = SizeClothes.objects.filter(id__in=stored_clothes)
            
        cart = []
        for clothe in clothes:
            quantity = 1
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
            })"""
        
        if "sizes_pk" in request.POST:
            print(stored_clothes)
            # delete a clothe in the cart
            clothe_to_delete = {"id":int(request.POST["sizes_pk"]), "cant":int(request.POST["sizes_cant"])}
            stored_clothes.remove(clothe_to_delete)
            request.session["cart_clothes"] = stored_clothes
            return HttpResponseRedirect("/sales-cart")
        

class CheckOutView(View):
    def get(self, request):
        stored_clothes = request.session.get("cart_clothes")
        print(stored_clothes)
        context = {}
        
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
            context["number"] = len(request.session.get("cart_clothes"))
            context["sum_prices"] = sum_prices
           
        return render(request, "clothes/checkout.html", context)

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

        return HttpResponseRedirect("/checkout")




















def cart(request):
    stored_clothes = request.session.get("cart_clothes")
    context = {}
    print(stored_clothes)
    if  stored_clothes is None or len(stored_clothes)==0:
        context["carts"] = []
        context["has_clothes"] = False

    else:
            
        clothes = SizeClothes.objects.filter(id__in=stored_clothes)
            
        cart = []
        for clothe in clothes:
            quantity = 1
            total_price = quantity*clothe.color_clothe.clothes.price
            cart.append({
            "size_pk": clothe.pk,
            "name": clothe.color_clothe.clothes.name,
            "slug":clothe.color_clothe.clothes.slug,
            "size": clothe.size,
            "color": clothe.color_clothe.color,
            "img": clothe.color_clothe.main_image.url,
            "price": clothe.color_clothe.clothes.price,
            "quantity": quantity,
            "total_price": total_price
            })
            
        print(cart)
        sum_prices = sum([item["total_price"] for item in cart])
        
            
        if request.method == 'POST':
            print("true")
            
            stored_clothes = request.session.get("cart_clothes")
            if stored_clothes is None:
                stored_clothes = []

            if "sizes_clothes_pk" in request.POST:
                print(request.POST["sizes_clothes_pk"])
                sizes_clothes_id = int(request.POST["sizes_clothes_pk"])  
                if sizes_clothes_id not in stored_clothes:
                    stored_clothes.append(sizes_clothes_id)
                    request.session["cart_clothes"] = stored_clothes
                
            elif "sizes_pk" in request.POST:
                print(request.POST["sizes_pk"])
                stored_clothes.remove(int(request.POST["sizes_pk"]))
                request.session["cart_clothes"] = stored_clothes

            elif "plus" in request.POST:
                #print(json.loads(request.body))
                data = json.loads(request.body)  # Obtener los datos enviados por AJAX
                #print(data)
                size_pk = data.get('size_pk')
                accion = data.get('accion')
                for item in cart:
                        
                    if item['size_pk'] == size_pk:
                           
                        #if item['quantity'] > 0:  
                        if accion == 'incrementar':
                            item['quantity'] += 1
                        elif accion == 'decrementar' and item['quantity'] > 1:
                            item['quantity'] -= 1
                        item['total_price'] = item['quantity'] * item['price']  # Actualizar el total
             
                
      

                            # Guardar la lista actualizada en la sesión
                    request.session["cart_clothes"] = [item['size_pk'] for item in cart]
                    print(cart)
                            #return HttpResponseRedirect("/sales-cart")
                            # Respuesta en formato JSON para JavaScript
                    #return JsonResponse({'total_price': item['total_price'], 'quantity': item['quantity']})
            return HttpResponseRedirect("/sales-cart")       

              
        context["carts"] = cart
        context["has_clothes"] = True
        context["number"] = len(stored_clothes)
        context["sum_prices"] = sum_prices
           
    return render(request, "clothes/cart.html", context)
            
    
    