from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('product/', views.home, name="Home"),
    path('about/', views.about, name="About"),
    path('contact/', views.contact, name="Contact"),
    path('product/<int:product_id>', views.product_view, name="Product View"),
    path('submit/', views.submit, name="Submit"),
    path('checkout/', views.checkout, name="Checkout"),
    path('tracker/', views.tracker, name="Tracker"),
    path('payment_status/', views.payment_status, name="Payment Status"),
    path('search/', views.search, name="Search"),
    path('signup/', views.user_signup, name="Signup"),
    path('login/', views.user_login, name="Login"),
    path('logout/', views.user_logout, name="Logout"),
    path('post_comment/', views.post_comment, name="Post Comment"),
]
