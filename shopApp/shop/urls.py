from . import views
from django.urls import path

app_name = 'shop'
urlpatterns = [
    path('category/<str:category_slug>', views.ProductList, name='ProductListByCategory'),
    path('product/<str:product_slug>/<int:id>', views.ProductDetail, name='ProductDetail'),
    path('product/cart/', views.ShowCartProduct, name='ShowCartProduct'),
    path('ajax/cart/remove/product', views.RemoveProductFromCart, name='RemoveProductFromCart'),
    path('ajax/cart/chage/product/count', views.ChangeProductCountInCart, name='ChangeProductCountInCart'),
    path('', views.ProductList, name='ProductList'),
]
