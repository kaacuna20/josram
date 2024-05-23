from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .models import Clothes, ImageClothes, SizeClothes
from .forms import ClotheForm, CommentForm, PriceForm
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q

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
        items_order = request.session.get("order_by")
        print(items_order)
        
        if items_order == None:
            items_order = "clothes__name"
        

       # Base QuerySet
        all_products = ImageClothes.objects.all()

        # Apply color filters if present
        if filter_session:
            color_filters = Q()
            for color in filter_session:
                color_filters |= Q(color=color)
            all_products = all_products.filter(color_filters)

        # Apply price filters if present
        if price_session:
            price_filters = Q(clothes__price__range=(price_session[0], price_session[1]))
            all_products = all_products.filter(price_filters)

        # Order the QuerySet
        all_products = all_products.order_by(items_order)

        len_cart = 0
        if self.request.session.get("cart_clothes") is not None:
            len_cart = len(self.request.session.get("cart_clothes"))


            
        paginator = Paginator(all_products, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        

        dict_order_by = {
                        "Alfabeticamente, A-Z": "clothes__name",
                         "Alfabeticamente, Z-A": "-clothes__name",
                         "Precio, de menor a mayor": "clothes__price", 
                         "Precio, de mayor a menor": "-clothes__price", 
                         "Fecha: reciente a antiguo(a": "-clothes__date", 
                         "Fecha, antiguo(a) a reciente": "clothes__date"
                    }
        
   
        context = {
            "clothes_number": all_products.count(),
            "number": len_cart,
            "colors": ImageClothes.objects.values("color").distinct,
            "order_by": dict_order_by,
            "price_form": PriceForm(),
            "nav_colors": filter_session,
            "nav_prices": price_session,
            'page_obj': page_obj
        }
        return render(request, "clothes/all-products.html", context)
   
    def post(self, request):
        filter_session = request.session.get("filters_colors")
        price_session = request.session.get("filters_price")
        items_order = request.session.get("order_by")
         
        
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

        if "item_order"  in request.POST:
            print(request.POST["item_order"])
            items_order = request.POST["item_order"]
            request.session["order_by"] = items_order
                
            
        return HttpResponseRedirect("/products/all")
################################################################
    
class ClothesByType(View):
    
    def get(self, request, slug_type):

        filter_session = request.session.get("filters_colors")
        price_session = request.session.get("filters_price")
        items_order = request.session.get("order_by")
        
        # Base QuerySet with slug_type filter
        type_clothes = ImageClothes.objects.filter(clothes__slug_type=slug_type)

        # Apply color filters if present
        if filter_session:
            color_filters = Q()
            for color in filter_session:
                color_filters |= Q(color=color)
            type_clothes = type_clothes.filter(color_filters)

        # Apply price filters if present
        if price_session:
            price_filters = Q(clothes__price__range=(price_session[0], price_session[1]))
            type_clothes = type_clothes.filter(price_filters)

        # Order the QuerySet
        type_clothes = type_clothes.order_by(items_order)


        len_cart = 0
        if self.request.session.get("cart_clothes") is not None:
            len_cart = len(self.request.session.get("cart_clothes"))

        paginator = Paginator(type_clothes, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        dict_order_by = {
                        "Alfabeticamente, A-Z": "clothes__name",
                         "Alfabeticamente, Z-A": "-clothes__name",
                         "Precio, de menor a mayor": "clothes__price", 
                         "Precio, de mayor a menor": "-clothes__price", 
                         "Fecha: reciente a antiguo(a": "-clothes__date", 
                         "Fecha, antiguo(a) a reciente": "clothes__date"
                    }
   
        context = {
            "clothes_number": type_clothes.count(),
            "type": slug_type,
            "number": len_cart,
            "colors": ImageClothes.objects.values("color").distinct,
            "order_by": dict_order_by,
            "price_form": PriceForm(),
            "nav_colors": filter_session,
            "nav_prices": price_session,
            'page_obj': page_obj
        }
        return render(request, "clothes/type-clothes.html", context)
    
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

        if "item_order"  in request.POST:
            print(request.POST["item_order"])
            items_order = request.POST["item_order"]
            request.session["order_by"] = items_order
            
        return HttpResponseRedirect("/collections/" + slug_type)



class ClothesByGender(View):
  
    def get(self, request, gender):

        filter_session = request.session.get("filters_colors")
        price_session = request.session.get("filters_price")
        items_order = request.session.get("order_by")

         # Base QuerySet with slug_type filter
        gender_clothes = ImageClothes.objects.filter(clothes__gender=gender)

        # Apply color filters if present
        if filter_session:
            color_filters = Q()
            for color in filter_session:
                color_filters |= Q(color=color)
            gender_clothes = gender_clothes.filter(color_filters)

        # Apply price filters if present
        if price_session:
            price_filters = Q(clothes__price__range=(price_session[0], price_session[1]))
            gender_clothes = gender_clothes.filter(price_filters)

        # Order the QuerySet
        gender_clothes = gender_clothes.order_by(items_order)

        
        
        len_cart = 0
        if self.request.session.get("cart_clothes") is not None:
            len_cart = len(self.request.session.get("cart_clothes"))

        paginator = Paginator(gender_clothes, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        dict_order_by = {
                        "Alfabeticamente, A-Z": "clothes__name",
                         "Alfabeticamente, Z-A": "-clothes__name",
                         "Precio, de menor a mayor": "clothes__price", 
                         "Precio, de mayor a menor": "-clothes__price", 
                         "Fecha: reciente a antiguo(a": "-clothes__date", 
                         "Fecha, antiguo(a) a reciente": "clothes__date"
                    }
   
        context = {
            "clothes": gender_clothes,
            "clothes_number": gender_clothes.count(),
            "gender": gender,
            "number": len_cart,
            "colors": ImageClothes.objects.values("color").distinct,
            "order_by": dict_order_by,
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

        if "item_order"  in request.POST:
            print(request.POST["item_order"])
            items_order = request.POST["item_order"]
            request.session["order_by"] = items_order
            
        return HttpResponseRedirect("/collection/" + gender)
    

class SearhView(View):
   
    def get(self, request):

        query = request.GET.get('q')
        split_query = query.split(" ") if query else []
        combined_results = SizeClothes.objects.none()  # Initialize an empty QuerySet

        if query:
            for q in split_query:
                result = SizeClothes.objects.filter(
                    Q(size__icontains=q) |
                    Q(color_clothe__color__icontains=q) |
                    Q(color_clothe__clothes__name__icontains=q) |
                    Q(color_clothe__clothes__type__icontains=q) |
                    Q(color_clothe__clothes__gender__icontains=q)       
                )
                combined_results = combined_results.union(result)  # Union with accumulated results

            # Remove duplicates manually
            seen = set()
            distinct_results = []
            for item in combined_results:
                identifier = item.color_clothe.color  # Use a tuple to identify unique items
                if identifier not in seen:
                    seen.add(identifier)
                    distinct_results.append(item)
        else:
            distinct_results = []

        len_cart = 0
        if self.request.session.get("cart_clothes") is not None:
            len_cart = len(self.request.session.get("cart_clothes"))

        context = {
            "query": query,
            "clothes": distinct_results,
            "clothes_number": len(distinct_results),
            "number": len_cart,
        }
        return render(request, "clothes/search_results.html", context)



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
                try:
                    sizes_clothes = SizeClothes.objects.get(color_clothe__clothes__slug=slug, color_clothe__color=post_color , size=post_size )
                    if int(request.POST["cant"]) > sizes_clothes.cant:
                        is_enough = False
                
                except Exception:
                    sizes_clothes = None
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
    





















    
    