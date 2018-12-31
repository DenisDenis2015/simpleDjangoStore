from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'shop'
urlpatterns = [
    path('category/<str:category_slug>', views.ProductList, name='ProductListByCategory'),
    path('product/<str:product_slug>/<int:id>', views.ProductDetail, name='ProductDetail'),
    path('product/<str:product_slug>/cart/<int:id>', views.AddProductToCart, name='AddProductToCart'),
    path('product/<str:product_slug>/cart/remove/<int:id>', views.RemoveProductFromCart, name='RemoveProductFromCart'),
    path('product/cart/', views.ShowCartProduct, name='ShowCartProduct'),
    path('', views.ProductList, name='ProductList'),
]
