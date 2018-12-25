from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ProductComment, Cart


# Страница с товарами
def ProductList(request, category_slug=None, products=None):
    category = None
    categories = Category.objects.all()

    if products is None :
        products = Product.objects.filter(available=True)

    cartCount = get_cart_count(request)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'cartCount': cartCount
    })


def get_cart_count(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(created_by=request.user).count()


# Страница с описанием товара
def ProductDetail(request, id, product_slug):
    product = get_object_or_404(Product, id=id, slug=product_slug, available=True)
    product_comments = ProductComment.objects.filter(product_id=id).order_by('-created')
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=product.category_id)
    return render(request, 'shop/product/detail.html', {
        'product': product,
        'product_comments': product_comments,
        'categories': categories,
        'category': category,
    })


# Добавить продукт в корзину
def AddProductToCart(request, id, product_slug):
    product = get_object_or_404(Product, id=id, slug=product_slug, available=True)
    product.stock -= 1
    product.save()
    cart = Cart()
    cart.product = product
    cart.created_by = request.user
    cart.save()
    return ProductList(request)


# Посмотреть корзину с товарами
def ShowCartProduct(request):
    # TODO пределать на join
    cart = Cart.objects.filter(created_by=request.user)
    cart_id = [item.id for item in cart]
    products = Product.objects.filter(id__in = cart_id)
    return ProductList(request, products = products)