from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .forms import LoginForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Cart, CartItem, Product, Profile
from django.core.files.base import ContentFile
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def checkout_data(request):
    # Dummy logic, replace with actual handling of checkout data
    data = {'payment_method': 'dummy_payment_method'}

    return JsonResponse(data)

def checkout_data(request):
    total_price = 20000
    payment_method = 'gcash'

    # Assuming you have a list of products, you should include it in the data
    products = [
        {"name": "Product 1", "quantity": 2, "price": 10000},
        {"name": "Product 2", "quantity": 1, "price": 5000},
        # Add more products as needed
    ]

    data = {'payment_method': payment_method, 'total_price': total_price, 'products': products}

    request.session['checkout_data'] = data

    return JsonResponse(data)

def receipt(request):
    # Retrieve payment details, total_price, and products from the session
    checkout_data = request.session.get('checkout_data', {})
    
    payment_method = checkout_data.get('payment_method')
    transaction_id = "123456789"  # Replace with actual transaction ID
    total_price = checkout_data.get('total_price')
    products = checkout_data.get('products', [])

    return render(request, 'users/receipt.html', {
        'payment_method': payment_method,
        'transaction_id': transaction_id,
        'total_price': total_price,
        'products': products,
    })




def gcash(request):
    # Your view logic here
    return render(request, 'users/gcash.html')  # Assuming gcash.html is in the templates directory
def paymaya(request):
    # Your view logic here
    return render(request, 'users/paymaya.html')  # Assuming gcash.html is in the templates directory
def visa(request):
    # Your view logic here
    return render(request, 'users/visa.html')  # Assuming gcash.html is in the templates directory

# Create your views here.
def checkout(request):
    return render(request, 'users/checkout.html')

def home(request):
    return render(request, 'users/home.html')
def about(request):
    return render(request, 'users/about.html')
def contact(request):
    return render(request, 'users/contact.html')

def sign_up(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def sign_in(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})






def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('home')   




class UserProfile(View):
    template_name = 'users/profile.html'

    def get(self, request):
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user_profile = None
        form_data = {
            'name': user_profile.full_name if user_profile else '',
            'email': request.user.email if user_profile else '', 
            'designation': user_profile.designation if user_profile else '',
            'mobile_no': user_profile.mobile_number if user_profile else '',
            'profile_image': user_profile.profile_image if user_profile else '',
            'profile_summary': user_profile.profile_summary if user_profile else '',
            'city': user_profile.city if user_profile else '',
            'state': user_profile.state if user_profile else '',
            'country': user_profile.country if user_profile else '',
        }
        context = {
        'profile': user_profile,
        'form_data': form_data
        }
        return render(request, self.template_name, context)

    def post(self, request):
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user_profile = None
        uploaded_image = request.FILES.get('profile_image', None)
        if uploaded_image:
            user_profile.profile_image.save(uploaded_image.name, ContentFile(uploaded_image.read()))
        full_name = request.POST.get('name')
        email = request.POST.get('email') 
        designation = request.POST.get('designation')
        mobile_number = request.POST.get('mobile_no')
        profile_summary = request.POST.get('profile_summary')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')

        if user_profile:
            user_profile.full_name = full_name
            user_profile.designation = designation
            user_profile.mobile_number = mobile_number
            user_profile.profile_summary = profile_summary
            user_profile.city = city
            user_profile.state = state
            user_profile.country = country
            user_profile.save()

       
            user_profile.user.email = email
            user_profile.user.save()

        return redirect('user-profile') 
    


def product_list(request):
    products = Product.objects.all()
    return render(request, 'users/product_list.html', {'products': products})


def search_feature(request):
    # Check if the request is a post request.
    if request.method == 'POST':
        # Retrieve the search query entered by the user
        search_query = request.POST['search_query']
        # Filter your model by the search query
        products = Product.objects.filter(name__contains=search_query)
        return render(request, 'users/product_list.html', {'query':search_query, 'products':products})
    else:
        return render(request, 'users/product_list.html',{})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'users/product_details.html', {'product': product})


@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('product-list')


@login_required(login_url='login')
def remove_from_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = Cart.objects.get(user=request.user)
    try:
        cart_item = cart.cartitem_set.get(product=product)
        if cart_item.quantity >= 1:
             cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    
    return redirect('cart')


@login_required(login_url='login')
def view_cart(request):
    cart = request.user.cart
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'users/cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required(login_url='login')
def increase_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.user.cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')

@login_required(login_url='login')
def decrease_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.user.cart
    cart_item = cart.cartitem_set.get(product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

@login_required(login_url='login')
def fetch_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = request.user.cart
        cart_count = CartItem.objects.filter(cart=cart).count()
    return JsonResponse({'cart_count': cart_count})


def get_cart_count(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart=request.user.cart)
        cart_count = cart_items.count()
    else:
        cart_count = 0
    return cart_count