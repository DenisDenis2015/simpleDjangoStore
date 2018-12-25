from django.test import TestCase, TransactionTestCase

from shop.models import Category, Product, Cart
from django.urls import reverse
import shop.tests.helper.test_objects as t
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class ProductListByCategoryVewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        t.init_category()
        t.init_products()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def category_count_in_view_equals_category_count_in_model(self):
        resp = self.client.get('/')
        categories = Category.objects.all()
        self.assertTrue(resp.context['categories'].__len__() == categories.__len__())

    def test_view_url_exists_at_desired_location_category(self):
        categories = Category.objects.all()
        for category in categories:
            resp = self.client.get('/category/' + category.slug)
            self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name_product_list(self):
        resp = self.client.get(reverse('shop:ProductList'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_product_list(self):
        resp = self.client.get(reverse('shop:ProductList'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'shop/product/list.html')

    def test_view_url_accessible_by_name_product_list_by_category(self):
        categories = Category.objects.all()
        for category in categories:
            resp = self.client.get(reverse('shop:ProductListByCategory', args=[category.slug]))
            self.assertEqual(resp.status_code, 200)
            self.assertTemplateUsed(resp, 'shop/product/list.html')

    def test_count_of_product_in_db_equals_count_of_product_in_view(self):
        categories = Category.objects.all()
        for category in categories:
            products = Product.objects.filter(category=category)
            resp = self.client.get(reverse('shop:ProductListByCategory', args=[category.slug]))
            self.assertEqual(resp.status_code, 200)
            self.assertTrue(resp.context['products'].__len__() == products.__len__())


class ProductDetailVewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        t.init_category()
        t.init_products()

    def test_view_url_exists_at_desired_location_category(self):
        for product in Product.objects.all():
            resp = self.client.get(
                reverse('shop:ProductDetail', kwargs={'product_slug': product.slug, 'id': product.id}))
            self.assertEqual(resp.status_code, 200)
            self.assertTemplateUsed(resp, 'shop/product/detail.html')


class ShowCartProductViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        t.init_category()
        t.init_products()

    @classmethod
    def setUp(self):
        user = get_user_model()
        user.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='temporary', password='temporary')
        resp = self.client.get(reverse('shop:ShowCartProduct'))
        self.assertEqual(resp.status_code, 200)

    def test_view_url_redirect_user_if_not_login_to_login_page(self):
        resp = self.client.get(reverse('shop:ShowCartProduct'))
        # check redirect url
        self.assertEqual(resp.status_code, 302)
        self.assertTrue('/accounts/login/' in resp.url)

    # тест на отображение одного рподукта в корзтине
    def test_product_in_cart_avaliable(self):
        self.client.login(username='temporary', password='temporary')
        user = User.objects.get(username="temporary")
        t.add_product_to_cart(user)
        cart = Cart.objects.filter(created_by=user)
        self.assertTrue(cart.__len__() == 1)
        resp = self.client.get(reverse('shop:ShowCartProduct'))
        self.assertTrue(resp.context['products'].__len__() == 1)

    # тест на отображение нескольких продуктов в корзине
    def test_product_in_cart_avaliable_list(self):
        self.client.login(username='temporary', password='temporary')
        user = User.objects.get(username="temporary")
        t.add_product_to_cart(user, count=5)
        cart = Cart.objects.filter(created_by=user)
        self.assertTrue(cart.__len__() == 5)
        resp = self.client.get(reverse('shop:ShowCartProduct'))
        self.assertTrue(resp.context['products'].__len__() == 5)
