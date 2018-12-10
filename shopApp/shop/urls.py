from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'shop'
urlpatterns = [
    path('category/<str:category_slug>', views.ProductList, name='ProductListByCategory'),
    path('product/<str:product_slug>/<int:id>', views.ProductDetail, name='ProductDetail'),
    path('', views.ProductList, name='ProductList'),
]
