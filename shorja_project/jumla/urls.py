
from django.urls import path, include
from .views import *

# urls
urlpatterns = [
    path('', shopper.home, name="home"),
    path('Account/', include([
        path('login/', Account.login_view, name="login"),
        path('register/', Account.register_view, name="register"),
        path('change_password/', Account.change_password, name="change_password"),
    ])),
    path('shopper/', include([
        path('shopper/home', shopper.home, name="shopper_home"),
    ])),

]

# APIs
