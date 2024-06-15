<div class="row ">
	<div class="col ">
		<h1  style="color:#C6AB7C; font-size: 80px; font-weight:bold;">JOSRAM.col</h1>
	</div>
</div>

<h4 align="justify">This is a project developed by a client who need an interactive website to sell sport clothes by both gender, with the consent of the client, I share the project to public.</h4> 

### Features of aplication

- Website must have a navbar with overview of services offer JOSRAM, divide them in categories;
- Users can filter the products according to your search requirements, like gender, price and colors;
- Page has a blog section where JOSRAM share reflections on health and fitness;
- page must show a section about policies of business;
- Show the detail products and able to add the cart or buy directly acording the size, color and quantity in a dynamic way, and restrict and show buyer if product is not avaible;
- Offer different payment methods, using a platform and interact directly with buyer, create a notification system using email and SMS;
- Give a josram staff the control to post in blog, mount the entire stock in the database and view the opinions of their clients;

### Choose the tool

This project I choosed Django because the schema and panel admin is going to be useful to comply with the client requirements.

## Table of Contents
- [Project Structure](#Project-Structure)
- [Directory and File Descriptionsn](#Directory-and-File-Descriptions)
- [Getting Started](#Getting-Started)
- [Configuration](#Configuration)
- [Directory and File Descriptions](#Directory-and-File-Descriptions)
- [Integrating MercadoPago Checkout Pro](#Integrating-MercadoPago-Checkout-Pro)
  
## Project Structure
```ini
josram/
├── static/
│   ├── base.css
│   └── title-logo-josram.png
├── db.sqlite3
├── templates/
│   └── base.html
├── josram/
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
|   ├── settings.py
│   └── urls.py
│
├── clothes/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
|   ├── forms.py
|   ├── middleware.py.py
|   ├── models.py
|   ├── test.py
|   ├── urls.py
|   ├── views.py
|   ├── migrations/
│   ├── templates/clothes/
│   │   ├── all-products.html
│   │   ├── clothes-details.html
│   │   ├── follow.html
│   │   ├── gender-clothes.html
│   │   ├── index.html
│   │   ├── search_results.html
│   │   ├── type-clothes.html
│   │   └── includes/
|   │       ├── footers.html
|   │       ├── header-filter.html
|   │       ├── header.html
|   │       └── style.html
|   ├── static/clothes/
│   │   ├── all-products.css
│   │   ├── clothes-details.css
│   │   ├── follow.html
│   │   ├── comments.css
│   │   ├── index.css
│   │   ├── footer.css
│   │   ├── show-clothes.css
│   │   └── images/
│   └── templatetags/
│      ├── __init_.py
│      └── custom_filters.py
├── cart/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
|   ├── forms.py
|   ├── sms_utils.py
|   ├── email_utils.py
|   ├── middleware.py
|   ├── models.py
|   ├── test.py
|   ├── urls.py
|   ├── views.py
|   ├── migrations/
│   ├── templates/cart/
│   │   ├── checkout.html
│   │   ├── direct-payment-form.html
│   │   ├── failure.html
│   │   ├── form-payment.html
│   │   ├── my-cart.html
│   │   ├── pending.html
│   │   ├── success.html
│   │   └── includes/
|   │       └── style.html
|   └── static/cart/
│       ├── all-products.css
│       ├── checkout.css
│       └── logos/
├── blog/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
|   ├── forms.py
|   ├── models.py
|   ├── test.py
|   ├── urls.py
|   ├── views.py
|   ├── migrations/
│   ├── templates/blog/
│   │   ├── blog.html
│   │   ├── post-detail.html
|   └── static/blog/
│       ├── comments.css
│       └── images/
├── policies/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
|   ├── forms.py
|   ├── models.py
|   ├── test.py
|   ├── urls.py
|   ├── views.py
|   ├── migrations/
│   └── templates/policies/
│       ├── changes-devolutions.html
│       ├── privacity.html
│       ├── shipments.html
│       └── terms-and-conditions.html
│
├── venv/   
├── manage.py  
├── requirements.txt
└── .env
```

## Configuration

Create a `.env` file in the root directory of your project with the following variables:

```ini
# .env file
SECRET_KEY=JOSRAM_SECRET_KEY
EMAIL_PASSWORD=JOSRAM_PASSWORD_APP
JOSRAM_EMAIL=JOSRAM_EMAIL_APP
TWILIO_ACCOUNT_SID=JOSRAM_TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN=JOSRAM_TWILIO_AUTH_TOKEN
JOSRAM_NUMBER=JOSRAM_NUMBER_PHONE
MERCADOPAGO_ACCESS_TOKEN=YOUR_ACCESS_TOKEN
HTTPS_PROXY=NGROK_HTTPS_URL
```

## Directory and File Descriptions

- `static/`: Contains static files such as CSS and images used across the entire project.
  - `base.css`: Base stylesheet for the project.
  - `title-logo-josram.png`: Logo image for the project.

- `db.sqlite3`: SQLite database file for the project.

- `templates/`: Contains global HTML templates.
  - `base.html`: Base template for the project.

- `josram/`: Main Django project directory.
  - `__init__.py`: Initializes the module.
  - `asgi.py`: ASGI configuration for the project.
  - `wsgi.py`: WSGI configuration for the project.
  - `settings.py`: Settings/configuration for the project.
  - `urls.py`: URL routing for the project.

- `clothes/`: Django app for managing clothes.
  - `__init__.py`: Initializes the module.
  - `admin.py`: Admin interface configuration.
  - `apps.py`: App configuration.
  - `forms.py`: Forms used in the clothes app.
  - `middleware.py`: Middleware for the clothes app.
  - `models.py`: Database models for the clothes app.
  - `test.py`: Tests for the clothes app.
  - `urls.py`: URL routing for the clothes app.
  - `views.py`: Views for the clothes app.
  - `migrations/`: Database migrations for the clothes app.
  - `templates/clothes/`: HTML templates specific to the clothes app.
    - `all-products.html`: Template for displaying all products.
    - `clothes-details.html`: Template for displaying details of a specific clothing item.
    - `follow.html`, `gender-clothes.html`, `index.html`, `search_results.html`, `type-clothes.html`: Other specific templates.
    - `includes/`: Reusable template fragments.
      - `footers.html`, `header-filter.html`, `header.html`, `style.html`: Common reusable fragments.
  - `static/clothes/`: Static files specific to the clothes app.
    - CSS files for different parts of the clothes app.
    - `images/`: Directory for images used in the clothes app.
  - `templatetags/`: Custom template tags and filters.
    - `__init_.py`: Initializes the module.
    - `custom_filters.py`: Custom template filters.

- `cart/`: Django app for managing the shopping cart and checkout process.
  - Similar structure to the `clothes/` app, but specific to cart functionality.
  - Includes templates for checkout, payment forms, and cart views.

- `blog/`: Django app for managing blog posts.
  - Similar structure to the `clothes/` app, but specific to blog functionality.
  - Includes templates for blog views and post details.

- `policies/`: Django app for managing site policies.
  - Similar structure to the `clothes/` app, but specific to policies.
  - Includes templates for different policies like privacy, terms, and conditions.

- `venv/`: Virtual environment directory for managing project dependencies.

- `manage.py`: Command-line utility for managing the Django project.

- `requirements.txt`: List of project dependencies.

- `.env`: Environment variables configuration file.

## Getting Started

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/josram.git
    ```
2. **Navigate to the project directory**:
    ```sh
   cd josram
    ```
3. **Create a virtual environment**:
   ```sh
   python -m venv venv
    ```
4. **Activate the virtual environment**:
   -On Windows:
     ```sh
     venv\Scripts\activate
      ```
   -On macOS/Linux:
    ```sh
     source venv/bin/activate
      ```
5. **Install the dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
6. **Run the database migrations**:
    ```sh
   python manage.py migrate
   ```
7. **Start the development server**:
    ```sh
   python manage.py runserver
   ```
8. **Start the development server**:
 - Open your web browser and go to http://localhost:8000.

## Integrating MercadoPago Checkout Pro

This website, offer payment method using mercadopago to online payment, and I integrated the SDK that is a solution that allows your customers to make purchases through Mercado Pago payment pages safely, quickly and with the possibility of paying with the main payment methods currently available. 

I share the documentation: https://www.mercadopago.com.co/developers/es/docs/checkout-pro/landing

Step 1: Install the MercadoPago SDK
- Add the MercadoPago SDK to your `requirements.txt` file.

Step 2: Configure MercadoPago
- Add your MercadoPago credentials to the `.env` file.

Step 3: Create a Payment View
- In your `cart` app, create a view to handle the payment process. For example, in `cart/views.py`.

Step 3: Set Up ngrok for HTTPS Connection
To enable HTTPS for your local development environment, use ngrok. ngrok exposes your local server to the internet securely.
1. Install ngrok:
    Download and install ngrok from ngrok.com.
2. Start ngrok:
    Run ngrok on the port your Django server is running on (usually 8000):
```ini
ngrok http 8000
```
3. Update Callback URLs:
   Copy the generated HTTPS URL from ngrok and use it to update the callback URLs in your code.
   
Step 4: Create a Test Seller Account in MercadoPago
To test your integration, create a test seller account in MercadoPago:

1. Create Test Users:
    Go to the MercadoPago Developers site and create test users. This will give you both seller and buyer test accounts.

2. Use Production Credentials:
    Ensure you have the production MercadoPago credentials for API testing.

Step 5: Create a Payment View
In your `cart` app, create a view to handle the payment process. For example, in `cart/views.py`:

```ini
import mercadopago
import os
from django.shortcuts import render, redirect
from django.conf import settings

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
      
        sdk = mercadopago.SDK(os.getenv('MERCADOPAGO_ACCESS_TOKEN'))
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
                "success": f"https://{os.getenv('HTTPS_PROXY')}/cart/success",
                "failure": f"https://{os.getenv('HTTPS_PROXY')}/cart/failure",
                "pending": f"https://{os.getenv('HTTPS_PROXY')}/cart/pending"
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
            "notification_url": f"https://{os.getenv('HTTPS_PROXY')}/cart/notification",
         
            "expires": True,
            "expiration_date_from": f"{expiration_date_from.isoformat()}",
            "expiration_date_to": f"{expiration_date_to.isoformat()}"
        }
        
        preference_response = sdk.preference().create(preference_data)
        if preference_response.get("status") != 201:
            return JsonResponse(preference_response, status=preference_response.get("status", 400))
        preference = preference_response["response"]
    
        return HttpResponseRedirect(f"{preference['init_point']}")
```

Step 6: Add URLs
Add a URL pattern for the new payment view in `cart/urls.py`:
```ini
from django.urls import path
from . import views

urlpatterns = [
    path("payment-methods", views.ReferenceView.as_view(), name="mercadopago-payment"),
    # other paths...
]
```

Step 7: Update Templates
Update your checkout.html template to include the MercadoPago checkout button:
```ini

<form id="payment-form" class="needs-validation" method="POST" action="{% url 'mercadopago-payment' %}" novalidate>
          {% csrf_token %}
	# elements of form...

<button id="checkout-button" class="w-100 btn btn-primary btn-lg mt-5" type="submit" style="background-color:black;">Ir a pagar</button>
</form>
<script>
  document.getElementById('payment-form').addEventListener('submit', function (e) {
    var form = this;
    var mercadopagoRadio = document.getElementById('mercadopagoRadio');
    var directRadio = document.getElementById('directRadio');
    if (mercadopagoRadio.checked) {
      form.action = "{% url 'mercadopago-payment' %}";
    } else if (directRadio.checked) {
      form.action = "{% url 'direct-payment' order_josram %}";
    }
  });
</script>
```

Step 8: Handle Payment Responses
Create views to handle success, failure, and pending payment responses in `cart/views.py`:

```ini

def payment_success(request):
    return render(request, 'cart/success.html')

def payment_failure(request):
    return render(request, 'cart/failure.html')

def payment_pending(request):
    return render(request, 'cart/pending.html')
```
And add corresponding URLs in `cart/urls.py`:

```ini
    path("success", views.success),
    path("failure", views.failure),
    path("pending", views.supend),
```
Step 9: Test Your Integration
1. Start your Django server:
```ini
python manage.py runserver
```
2. Start ngrok:
```ini
ngrok http 8000
```
3. Test with MercadoPago's Test User:
    Use the test buyer account created earlier to simulate a purchase.
   
Now project is set up to handle payments using MercadoPago's Checkout Pro. Be sure to test the integration thoroughly before going live.
