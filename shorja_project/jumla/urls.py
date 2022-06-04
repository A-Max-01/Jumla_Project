
from django.urls import path, include
from .views import *

# urls
urlpatterns = [
    path('', shopper.home, name="home"),
    path('Account/', include([

        path('register/', Account.register_view, name="register"),
        path('login/', Account.login_view, name="login"),
        # path('', include('django.contrib.auth.urls')),
        path('logout/', Account.logout_view, name="logout"),
        path('change_password/', Account.change_password, name="change_password"),
    ])),
    path('shopper/', include([
        path('brows_bills', shopper.show_cart_bills_order, name="brows_bills"),
        # APIs
        path('add-to-cart', shopper.add_to_cart, name="add_to_cart"),
        path('update_quentity', shopper.update_quentity, name="update_quentity"),
        path('check_item_in_bill_order', shopper.check_item_in_bill_order, name="check_item_in_bill_order"),

    ])),

]

