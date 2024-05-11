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
from django.core.paginator import Paginator

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
        len_cart = 0
        if self.request.session.get("cart_clothes") is not None:
            len_cart = len(self.request.session.get("cart_clothes"))

        context = super().get_context_data(**kwargs)
        context["number"] = len_cart
        return context

class AllProducts(View):
    
    def get(self, request):

        filter_session = request.session.get("filters_colors")
        price_session = request.session.get("filters_price")
        

        if  (filter_session is None or len(filter_session)==0) and (price_session is None or len(price_session)==0):
            all_products = ImageClothes.objects.all()

        elif filter_session:
            queryset_union = ImageClothes.objects.none()
            for color in filter_session:
                queryset_color = ImageClothes.objects.filter(color=color)
                # Join with existing QuerySet
                queryset_union = queryset_union.union(queryset_color)
            all_products = queryset_union.all()

        elif price_session:
            all_products = ImageClothes.objects.filter(clothes__price__range=(price_session[0], price_session[1]))

        else:
            queryset_union = ImageClothes.objects.none()
            price_filter = ImageClothes.objects.filter(clothes__price__range=(price_session[0], price_session[1]))
            for color in filter_session:
                queryset_color = ImageClothes.objects.filter(color=color)
                # Join with existing QuerySet
                queryset_union = queryset_union.union(queryset_color)
            all_products = queryset_union.intersection(price_filter)

        len_cart = 0
        if self.request.session.get("cart_clothes") is not None:
            len_cart = len(self.request.session.get("cart_clothes"))

        paginator = Paginator(all_products, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
   
        context = {
            "clothes": all_products,
            "clothes_number": all_products.count(),
            "number": len_cart,
            "colors": ImageClothes.objects.values("color").distinct,
            "price_form": PriceForm(),
            "nav_colors": filter_session,
            "nav_prices": price_session,
            'page_obj': page_obj
        }
        return render(request, "clothes/all-products.html", context)
    
    def post(self, request):
        filter_session = request.session.get("filters_colors")
        price_session = request.session.get("filters_price")

        if filter_session is None:
            filter_session = []

        if price_session is None:
            price_session = []
       

        if "color_filter" in request.POST:
            color_filter = request.POST["color_filter"]
            
            if color_filter not in filter_session:
                filter_session.append(color_filter)
                # save it in the session
                request.session["filters_colors"] = filter_session

        if "filter_price" in request.POST:
            min_price = int(request.POST["price_low"])
            max_price =int(request.POST["price_hight"])
            price_session = (min_price, max_price)
            request.session["filters_price"] = price_session
           
        elif "delete_filters" in request.POST:
            filter_session.clear()
            price_session.clear()
            request.session["filters_colors"] = filter_session
            request.session["filters_price"] = price_session

        elif "delete_color" in request.POST:
            filter_session.remove(request.POST["color"])
            request.session["filters_colors"] = filter_session

        elif "delete_price" in request.POST:
            price_session.clear()
            request.session["filters_price"] = price_session
            
        return HttpResponseRedirect("/products/all")
################################################################
    
class ClothesByType(View):
    
    def get(self, request, slug_type):

        filter_session = request.session.get("filters_colors")
        price_session = request.session.get("filters_price")

        if  (filter_session is None or len(filter_session)==0) and (price_session is None or len(price_session)==0):
            type_clothes = ImageClothes.objects.filter(clothes__slug_type=slug_type)

        elif filter_session:
            queryset_union = ImageClothes.objects.none()
            for color in filter_session:
                queryset_color = ImageClothes.objects.filter(clothes__slug_type=slug_type, color=color)
                # Join with existing QuerySet
                queryset_union = queryset_union.union(queryset_color)
            type_clothes = queryset_union.all()

        elif price_session:
            type_clothes = ImageClothes.objects.filter(clothes__slug_type=slug_type, clothes__price__range=(price_session[0], price_session[1]))

        else:
            queryset_union = ImageClothes.objects.none()
            price_filter = ImageClothes.objects.filter(clothes__slug_type=slug_type, clothes__price__range=(price_session[0], price_session[1]))
            for color in filter_session:
                queryset_color = ImageClothes.objects.filter(clothes__slug_type=slug_type, color=color)
                # Join with existing QuerySet
                queryset_union = queryset_union.union(queryset_color)
            type_clothes = queryset_union.intersection(price_filter)

        len_cart = 0
        if self.request.session.get("cart_clothes") is not None:
            len_cart = len(self.request.session.get("cart_clothes"))

        paginator = Paginator(type_clothes, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
   
        context = {
            
            "clothes": type_clothes,
            "clothes_number": type_clothes.count(),
            "type": slug_type,
            "number": len_cart,
            "colors": ImageClothes.objects.values("color").distinct,
            "price_form": PriceForm(),
            "nav_colors": filter_session,
            "nav_prices": price_session,
            'page_obj': page_obj
        }
        return render(request, "clothes/all-products.html", context)
    
    def post(self, request, slug_type):
        filter_session = request.session.get("filters_colors")
        price_session = request.session.get("filters_price")

        if filter_session is None:
            filter_session = []

        if price_session is None:
            price_session = []
       

        if "color_filter" in request.POST:
            color_filter = request.POST["color_filter"]
            
            if color_filter not in filter_session:
                filter_session.append(color_filter)
                # save it in the session
                request.session["filters_colors"] = filter_session

        if "filter_price" in request.POST:
            min_price = int(request.POST["price_low"])
            max_price =int(request.POST["price_hight"])
            price_session = (min_price, max_price)
            request.session["filters_price"] = price_session
           
        elif "delete_filters" in request.POST:
            filter_session.clear()
            price_session.clear()
            request.session["filters_colors"] = filter_session
            request.session["filters_price"] = price_session

        elif "delete_color" in request.POST:
            filter_session.remove(request.POST["color"])
            request.session["filters_colors"] = filter_session

        elif "delete_price" in request.POST:
            price_session.clear()
            request.session["filters_price"] = price_session
            
        return HttpResponseRedirect("/collections/" + slug_type)



class ClothesByGender(View):
    
    def get(self, request, gender):

        filter_session = request.session.get("filters_colors")
        price_session = request.session.get("filters_price")


        if  (filter_session is None or len(filter_session)==0) and (price_session is None or len(price_session)==0):
            gender_clothes = ImageClothes.objects.filter(clothes__gender=gender)

        elif filter_session:
            queryset_union = ImageClothes.objects.none()
            for color in filter_session:
                queryset_color = ImageClothes.objects.filter(clothes__gender=gender, color=color)
                # Join with existing QuerySet
                queryset_union = queryset_union.union(queryset_color)
            gender_clothes = queryset_union.all()

        elif price_session:
            gender_clothes = ImageClothes.objects.filter(clothes__gender=gender, clothes__price__range=(price_session[0], price_session[1]))

        else:
            queryset_union = ImageClothes.objects.none()
            price_filter = ImageClothes.objects.filter(clothes__gender=gender, clothes__price__range=(price_session[0], price_session[1]))
            for color in filter_session:
                queryset_color = ImageClothes.objects.filter(clothes__gender=gender, color=color)
                # Join with existing QuerySet
                queryset_union = queryset_union.union(queryset_color)
            gender_clothes = queryset_union.intersection(price_filter)
        
        len_cart = 0
        if self.request.session.get("cart_clothes") is not None:
            len_cart = len(self.request.session.get("cart_clothes"))

        paginator = Paginator(gender_clothes, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
   
        context = {
            "clothes": gender_clothes,
            "clothes_number": gender_clothes.count(),
            "gender": gender,
            "number": len_cart,
            "colors": ImageClothes.objects.values("color").distinct,
            "price_form": PriceForm(),
            "nav_colors": filter_session,
            "nav_prices": price_session,
            'page_obj': page_obj
        }
        return render(request, "clothes/gender-clothes.html", context)
    
    def post(self, request, gender):
        filter_session = request.session.get("filters_colors")
        price_session = request.session.get("filters_price")

        if filter_session is None:
            filter_session = []

        if price_session is None:
            price_session = []
       

        if "color_filter" in request.POST:
            color_filter = request.POST["color_filter"]
            print(color_filter)
            if color_filter not in filter_session:
                filter_session.append(color_filter)
                # save it in the session
                request.session["filters_colors"] = filter_session

        if "filter_price" in request.POST:
            min_price = int(request.POST["price_low"])
            max_price =int(request.POST["price_hight"])
            price_session = (min_price, max_price)
            request.session["filters_price"] = price_session
           
        elif "delete_filters" in request.POST:
            filter_session.clear()
            price_session.clear()
            request.session["filters_colors"] = filter_session
            request.session["filters_price"] = price_session

        elif "delete_color" in request.POST:
            filter_session.remove(request.POST["color"])
            request.session["filters_colors"] = filter_session

        elif "delete_price" in request.POST:
            price_session.clear()
            request.session["filters_price"] = price_session
            
        return HttpResponseRedirect("/collection/" + gender)


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

    len_cart = 0
    if request.session.get("cart_clothes") is not None:
        len_cart = len(request.session.get("cart_clothes"))
    
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
                    "number": len_cart,
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
            "number": len_cart,
            "added_cart": added_cart
        }
    return render(request, "clothes/clothes-details.html", context)
    


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





















    
    