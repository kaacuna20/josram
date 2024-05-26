from django.shortcuts import render

# Create your views here.

def change_devolutions(request):
    len_cart = 0
    if request.session.get("cart_clothes") is not None:
        len_cart = len(request.session.get("cart_clothes"))
    return render(request, "policies/changes-devolutions.html", {"number": len_cart})

def privacity(request):
    len_cart = 0
    if request.session.get("cart_clothes") is not None:
        len_cart = len(request.session.get("cart_clothes"))
    return render(request, "policies/privacity.html", {"number": len_cart})

def shipments(request):
    len_cart = 0
    if request.session.get("cart_clothes") is not None:
        len_cart = len(request.session.get("cart_clothes"))
    return render(request, "policies/shipments.html", {"number": len_cart})

def terms_and_conditions(request):
    len_cart = 0
    if request.session.get("cart_clothes") is not None:
        len_cart = len(request.session.get("cart_clothes"))
    return render(request, "policies/terms-and-conditions.html", {"number": len_cart})
