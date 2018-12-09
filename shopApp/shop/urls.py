from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'shop'
urlpatterns = [
    path('<str:category_slug>', views.ProductList, name='ProductListByCategory'),
    path('<int:id>/<str:slug>', views.ProductDetail, name='ProductDetail'),
    path('', views.ProductList, name='ProductList'),
]
