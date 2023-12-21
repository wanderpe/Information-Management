from django.contrib import admin
from .models import Profile
from .models import Profile, Product, Cart, CartItem
from .models import PaymentReceipt

# Register your models here.

admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(PaymentReceipt)

