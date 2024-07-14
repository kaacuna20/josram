from django.views.generic import TemplateView

# Create your views here.


class ChangeDevolutionView(TemplateView):
    template_name = "policies/changes-devolutions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Handle session data
        len_cart = 0
        if self.request.session.get("cart_clothes") is not None:
            len_cart = len(self.request.session.get("cart_clothes"))
        context["number"] = len_cart

        return context


class PrivacityView(TemplateView):
    template_name = "policies/privacity.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Handle session data
        len_cart = 0
        if self.request.session.get("cart_clothes") is not None:
            len_cart = len(self.request.session.get("cart_clothes"))
        context["number"] = len_cart

        return context


class ShipmentsView(TemplateView):
    template_name = "policies/shipments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Handle session data
        len_cart = 0
        if self.request.session.get("cart_clothes") is not None:
            len_cart = len(self.request.session.get("cart_clothes"))
        context["number"] = len_cart

        return context


class TermsConditionsView(TemplateView):
    template_name = "policies/terms-and-conditions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Handle session data
        len_cart = 0
        if self.request.session.get("cart_clothes") is not None:
            len_cart = len(self.request.session.get("cart_clothes"))
        context["number"] = len_cart

        return context


