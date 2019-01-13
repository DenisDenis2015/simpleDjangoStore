from shop.models import Category, Product, Cart
import uuid


def init_category():
    category = {'Книги': 'Knigi', 'Техника': 'Technika', 'Посуда': 'Posuda'}
    for key, value in category.items():
        Category.objects.create(name=key, slug=value)


def init_products():
    categories = Category.objects.all()
    for category in categories:
        for number in range(4):
            item = Product()
            item.category = category
            item.name = my_random_string(category.slug)
            item.slug = item.name + '_slug'
            item.price = 1
            item.stock = 2
            item.save()


def add_random_product():
    category = Category.objects.first()
    item = Product()
    item.category = category
    item.name = my_random_string(category.slug)
    item.slug = item.name + '_slug'
    item.price = 1
    item.stock = 2
    item.save()
    return item


def add_product_to_cart(user, product=None, count=1):
    for item in range(0, count):
        cart = Cart()
        if product is not None:
            cart.product = product
        else:
            cart.product = add_random_product()
        cart.created_by = user
        cart.save()


def my_random_string(string_start, string_length=6):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())  # Convert UUID format to a Python string.
    random = random.upper()  # Make all characters uppercase.
    random = random.replace("-", "")  # Remove the UUID '-'.
    return string_start + random[0:string_length]  # Return the random string.
