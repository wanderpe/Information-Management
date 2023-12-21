from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', UserProfile.as_view(), name='user-profile' ),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
    path('product-list/', product_list, name='product-list'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove-from-cart'),
    path('cart/', view_cart, name='cart'),
    path('increase-cart-item/<int:product_id>/', increase_cart_item, name='increase-cart-item'),
    path('decrease-cart-item/<int:product_id>/', decrease_cart_item, name='decrease-cart-item'),
    path('fetch-cart-count/', fetch_cart_count, name='fetch-cart-count'),
    path('search/', views.search_feature, name='search-view'),
    path('products/<int:product_id>/', views.product_detail, name='product_details'),
    path('cart/checkout.html', views.checkout, name='checkout'),
    path('checkout.html/gcash', gcash, name='gcash'),
    path('checkout.html/paymaya', paymaya, name='paymaya'),
    path('checkout.html/visa', visa, name='visa'),
    path('gcash/receipt', views.receipt, name='receipt'),
    path('paymaya/receipt', views.receipt, name='receipt'),
    path('visa/receipt', views.receipt, name='receipt'),
    path('checkout_data/', checkout_data, name='checkout_data'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),



]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)