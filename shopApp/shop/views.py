from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ProductComment


# Страница с товарами
def ProductList(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })


# Страница с описанием товара
def ProductDetail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    product_comments = ProductComment.objects.filter(product_id=id).order_by('-created')
    return render(request, 'shop/product/detail.html', {
        'product': product,
        'product_comments' : product_comments
    })
