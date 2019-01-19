from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Product, ProductComment, Cart
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse


def ProductList(request, category_slug=None, products=None, is_cart=False):
    """
     Страница с товарами
     :param request - запрос
     :param category_slug - название категории
     :param products - список продуктов которые необходимо отобразить
     :param is_cart - флаг, true если просматриваем содержимое корзины, false в обратном случаи
    """
    category = None
    categories = Category.objects.all()
    if products is None:
        products = Product.objects.filter(available=True)
    cart_count = get_cart_count(request)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'cartCount': cart_count,
        'is_cart': is_cart
    })


def get_cart_count(request):
    """
     Получить общее колличество товаров в корзине пользователя
    """
    if request.user.is_authenticated:
        return Cart.objects.filter(created_by=request.user).distinct('product_id').count()


def ProductDetail(request, id, product_slug):
    """
     Страница с описанием товара
    """
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


def AddProductToCart(request, id, product_slug):
    """
     Добавить продукт в корзину
    """
    add_product_to_cart(id, request)
    return ProductList(request)


def add_product_to_cart(id, request):
    """
    Увеличивает колличество определенного продукта
    :param id: идентификатор продукта
    :param request:  запрос
    :return:
    """
    product = get_object_or_404(Product, id=id, available=True)
    product.stock -= 1
    product.save()
    cart = Cart()
    cart.product = product
    cart.created_by = request.user
    cart.save()


def remove_product_from_cart(request, product_id):
    """
     Удалить продукт из корзины пользователя
     Данные метод удаляет продукт из корзины пользователя и добавляет
     удаленное коллличество товара на склад
     :param product_id - идентификатор товара
    """
    product = get_object_or_404(Product, id=product_id)
    product.stock += Cart.objects.filter(created_by=request.user, product_id=product_id).count()
    product.save()
    Cart.objects.filter(product_id=product_id, created_by=request.user).delete()
    pass


@csrf_exempt
@login_required(login_url='/accounts/login/')
def ShowCartProduct(request):
    """
    Посмотреть корзину с товарами
    """
    cart = Cart.objects.filter(created_by=request.user)
    product_ids_in_cart = [item.product_id for item in cart]
    products = Product.objects.filter(id__in=set(product_ids_in_cart))

    # для каждого продукта получаем его колличество в корзине
    for product in products:
        product.count_in_cart = product_ids_in_cart.count(product.id)

    return ProductList(request, products=products, is_cart=True)


@csrf_exempt
@login_required(login_url='/accounts/login/')
def RemoveProductFromCart(request):
    """
    Удалить товар из корзины
    """
    remove_product_from_cart(request, request.POST['id'])

    return JsonResponse({"cartCount": get_cart_count(request)})


def dicreaseProductCountInCartByOne(request, product_id):
    """
    Уменьшить колличество товара в корзине на 1
    :param request: запрос
    :param product_id: идентификатор товара который надо уменьшить
    :return:
    """
    cart = Cart.objects.filter(created_by=request.user, product_id=product_id).earliest('date_from')
    cart.delete()


@csrf_exempt
@login_required(login_url='/accounts/login/')
def ChangeProductCountInCart(request):
    """
    Данный метод изменяет колличество конкретного товара в корзине,
    уменьшает на один или увеличивает, возвращает новое колличество измененого товара в
    корзине и общее колличество товара в корзине как результат
    :param request: запрос
    :return: product_count оставшиеся колличество товара
    """

    product_id = request.POST['id']
    operation = request.POST['operation']

    if operation == "add":
        add_product_to_cart(product_id, request)
    elif operation == "remove":
        dicreaseProductCountInCartByOne(request, product_id)
    else:
        raise AttributeError('undefined operation' + operation)

    product_count = Cart.objects.filter(created_by=request.user, product_id=product_id).count()
    return JsonResponse({"productCount": product_count, "cartCount": get_cart_count(request)})
