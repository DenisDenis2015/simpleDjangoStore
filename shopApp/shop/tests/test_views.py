from django.test import TestCase

from shop.models import Category, Product
from django.urls import reverse
import shop.tests.test_objects as t


class ProductListByCategoryVewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # init random category
        t.init_category()

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
            resp = self.client.get('/' + category.slug)
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


class ProductDetailVewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        t.init_category()
        t.init_products()

    def test_view_url_exists_at_desired_location_category(self):
        for product in Product.objects.all():
            resp = self.client.get(reverse('shop:ProductDetail', kwargs={'id':product.id, 'product_slug' : product.slug}))
            self.assertEqual(resp.status_code, 200)
            self.assertTemplateUsed(resp, 'shop/product/detail.html')
