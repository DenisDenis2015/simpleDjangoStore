from django.db import models
from django.urls import reverse


# Модель категории
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('shop:ProductListByCategory', args=[self.slug])

    def __str__(self):
        return self.name


# Модель продукта
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', verbose_name="Категория", on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', null=True, blank=True, verbose_name="Изображение товара")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(verbose_name="На складе")
    available = models.BooleanField(default=True, verbose_name="Доступен")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        index_together = [
            ['id', 'slug']
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:ProductDetail', args=[self.slug, self.id])


# Коментарий к продукту
class ProductComment(models.Model):
    product = models.ForeignKey(Product, related_name='product_comment', verbose_name="Продукт",
                                on_delete=models.CASCADE)
    comment = models.TextField(blank=False, verbose_name="Коментарий")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления коментария")

    def __str__(self):
        return self.comment


# Класс рейтинг товара TODO
class Rating(models.Model):
    product = models.ForeignKey(Product, related_name='rating', verbose_name="Рейтинг", on_delete=models.CASCADE)
