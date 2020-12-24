from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.HomePage.as_view(), name='store-home'),
    path('all/', views.Products.as_view(), name='store-products'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('all/<int:pk>/', views.ProductDetail.as_view(), name='product'),
    path('category/<int:id>/', views.category_view, name='category'),
    path('update/', views.update_cart, name='update_cart'),
    path('confirm/', views.confirm_order, name='confirm'),
    path('checkout/done', views.confirmRedirect, name='confirm-redirect'),
    
]
