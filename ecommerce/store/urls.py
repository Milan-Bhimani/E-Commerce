from django.urls import path
from .views import add_to_cart, cart, checkout, update_cart, product_list, product_detail, process_checkout

# Optionally, create a new view for the home page
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='store/home.html'), name='home'),  # Add this line
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update/<int:product_id>/', update_cart, name='update_cart'),
    path('products/', product_list, name='product_list'),
    path('products/<int:id>/', product_detail, name='product_detail'),
    path('process-checkout/', process_checkout, name='process_checkout'),
]
