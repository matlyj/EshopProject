from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, User, Customer, Admin, Employee
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from .forms import CategoryForm, ProductForm
from django.contrib.auth.decorators import login_required, user_passes_test
from Authentication_app.views import login, register
from django.db.models import Q
from unidecode import unidecode


# Create your views here.
# request -> response
# views are request handler

# checks if user is employee or admin @user_passes_test(is_employee_or_admin, login_url='/Eshop_app/user/')
def is_employee_or_admin(user):
    is_employee = user.groups.filter(name='Employee').exists()
    is_admin = user.groups.filter(name='Admin').exists()
    return is_employee or is_admin


# checks if user is admin @user_passes_test(is_admin, login_url='/Eshop_app/user/')
def is_admin(user):
    return user.groups.filter(name='Admin').exists()


# This function will render homepage.html page
def homepage(request):
    return render(request, 'homepage.html',
                  context={
                      "all_products": Product.objects.all()
                  })


# cart
def cart(request):
    return render(request, 'cart.html')


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        cart = request.session.get('cart', {})
        if product_id in cart:
            cart[product_id]['quantity'] += 1
        else:
            cart[product_id] = {
                'name': product.name,
                'price': str(product.price),
                'quantity': 1
            }

        request.session['cart'] = cart
        return redirect('cart')  # Přesměrování na stránku košíku
    else:
        return HttpResponseNotAllowed(['POST'])  # Zpracování neplatných metod


def cart_view(request):
    cart = request.session.get('cart', {})
    total_price = 0

    for item in cart.values():
        total_price += float(item['price']) * item['quantity']

    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})


# user page
def user_page(request):
    return render(request, 'user_page.html',
                  context={
                      "products_to_edit": Product.objects.all(),
                      "categories": Category.objects.all(),
                  })


# maso
def maso(request):
    # Get all products from category
    maso_category = get_object_or_404(Category, id=2)
    maso_products = Product.objects.filter(category=maso_category)

    return render(request, 'maso.html', context={
        "maso": maso_products
    })


# mlecne a chlazene
def mlecne_a_chlazene(request):
    # Get all products from category
    mlecne_chlazene_category = get_object_or_404(Category, id=3)
    mlecne_chlazene_products = Product.objects.filter(category=mlecne_chlazene_category)

    return render(request, 'mlecne_a_chlazene.html', context={
        "mlecne_chlazene": mlecne_chlazene_products
    })


# ovoce
def ovoce(request):
    # Get all products from category
    ovoce_category = get_object_or_404(Category, id=1)
    ovoce_products = Product.objects.filter(category=ovoce_category)

    return render(request, 'ovoce.html', context={
        "ovoce": ovoce_products
    })


# mrazene
def mrazene(request):
    # Get all products from category
    mrazene_category = get_object_or_404(Category, id=4)
    mrazene_products = Product.objects.filter(category=mrazene_category)

    return render(request, 'mrazene.html', context={
        "mrazene": mrazene_products
    })


# product detail
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


# Edit product form
def is_employee(user):
    return user.groups.filter(name='Employee').exists()  # add condition for user


@login_required
@user_passes_test(is_employee_or_admin, login_url='/Eshop_app/user/')
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # if form is POST, is validated and if correct it will be saved
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            # return redirect('product_detail', pk=product.pk)  # Redirect back to product detail
            return redirect('user')  # Redirect back to user_page.html
    else:
        # form = ProductForm()
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})


# create product
@login_required
@user_passes_test(is_employee_or_admin, login_url='/Eshop_app/user/')
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user')  # Redirect back to user_page.html
    else:
        form = ProductForm()

    return render(request, 'create_product.html', {'form': form})


# delete product
@login_required
@user_passes_test(is_employee_or_admin, login_url='/Eshop_app/user/')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('user')  # redirect after delete

    return render(request, 'delete_product.html', {'product': product})


# Category create
@user_passes_test(is_admin, login_url='/Eshop_app/user/')
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('category_list')
            return redirect('user')

    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})


# Category list
def category_list(request):
    categories = Category.objects.all()
    print(f'Categories: {categories}')
    return render(request, 'category_list.html', {'categories': categories})


# Category update
@user_passes_test(is_admin, login_url='/Eshop_app/user/')
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('user')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form})


# Category delete
@user_passes_test(is_admin, login_url='/Eshop_app/user/')
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('user')
    return render(request, 'category_confirm_delete.html', {'category': category})


# search
def search_products(request):
    query = request.GET.get('q')  # get search request from the get parameters
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |  # search by name
            Q(description__icontains=query) |  # search by description
            Q(category__name__icontains=query)  # search by category
        )
    else:
        products = Product.objects.all()  # if not request get all products

    return render(request, 'search_results.html', {'products': products, 'query': query})


# autocomplete search
def product_autocomplete(request):
    query = request.GET.get('term', '')  # get search term
    results = []

    if query:
        # make searches lovercase and remove čřř ect.
        normalized_query = unidecode(query).lower()
        # search in products
        products = Product.objects.all()
        matching_products = [
            product.name for product in products
            if normalized_query in unidecode(product.name).lower()
        ]
        results.extend(matching_products[:10])

        # search in categories
        categories = Category.objects.all()
        matching_categories = [
            f"{category.name} (Kategorie)" for category in categories
            if normalized_query in unidecode(category.name).lower()  # Convert category name to lowercase
        ]
        results.extend(matching_categories[:10])

    return JsonResponse(results, safe=False)


# autocomplete redirect
def search_results(request):
    query = request.GET.get('q', '')
    products = []
    categories = []

    if query:
        normalized_query = unidecode(query)

        # search products and categories
        products = Product.objects.filter(name__icontains=normalized_query)
        categories = Category.objects.filter(name__icontains=normalized_query)

    return render(request, 'search_results.html', {
        'query': query,
        'products': products,
        'categories': categories
    })
