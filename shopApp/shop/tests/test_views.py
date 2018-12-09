from django.test import TestCase

from shop.models import Category
from django.urls import reverse


class ProductListByCategoryVewTest(TestCase):
    category = {'Книги': 'Knigi', 'Техника': 'Technika', 'Посуда': 'Posuda'}

    @classmethod
    def setUpTestData(cls):
        # init random category
        for key, value in cls.category.items():
            Category.objects.create(name=key, slug=value)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def category_count_in_view_equals_category_count_in_model(self):
        resp = self.client.get('/')
        self.assertTrue(resp.context['categories'].__len__() == self.category.__len__())

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
        for key, value in self.category.items():
            resp = self.client.get(reverse('shop:ProductListByCategory', args=[value]))
            self.assertEqual(resp.status_code, 200)
            self.assertTemplateUsed(resp, 'shop/product/list.html')


class ProductDetailVewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # init category
        # init product
        pass
