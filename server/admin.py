from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Wallet, PaymentMethod, Payment, Game


admin.site.register(User)
admin.site.register(Wallet)
admin.site.register(PaymentMethod)
admin.site.register(Payment)
admin.site.register(Game)
