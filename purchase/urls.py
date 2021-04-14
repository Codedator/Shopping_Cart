from django.urls import path
from . import views

app_name = 'purchase'
urlpatterns = [
    path('', views.item_details, name='item_details'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.update_item, name="update_item"),
    path('shopping_cart/update_item/', views.update_item, name="update_item"),
    path('checkout/process_order/', views.process_order, name='process_order'),
]
