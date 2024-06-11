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
