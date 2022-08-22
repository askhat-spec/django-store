from django.db import models
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible
from django.urls import reverse

from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail, Transpose


@deconstructible
class RandomFileName(object):
    def __init__(self, path):
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _, filename):

        extension = os.path.splitext(filename)[1]
        return self.path % (uuid4(), extension)


class Category(models.Model):
    """Категория товаров"""

    name = models.CharField('Название', max_length=255, db_index=True)
    slug = models.SlugField('URL', max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return self.id

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    """Товары магазина"""

    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, verbose_name='Категория', blank=True, null=True)
    article = models.CharField('Артикул', max_length=24, blank=True)
    name = models.CharField('Название', max_length=255, db_index=True)
    slug = models.SlugField('URL', max_length=255, unique=True, db_index=True)
    # _image = models.ImageField('Изображения товара', upload_to=RandomFileName('products'), blank=True)
    thumbnail = ProcessedImageField(
        upload_to=RandomFileName('products'),
        processors=[Transpose(), Thumbnail(400)],
        format='WEBP',
    )
    description = models.TextField('Описание товара', blank=True)
    price = models.PositiveIntegerField('Цена')
    old_price = models.PositiveIntegerField('Старая цена', blank=True, null=True)
    available = models.BooleanField('В наличии', default=True)
    created = models.DateTimeField('Создано', auto_now_add=True)
    updated = models.DateTimeField('Изменено', auto_now=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

    def get_profit(self):
        try:
            return 100 - round(self.price * 100 / self.old_price)
        except:
            return False

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImage(models.Model):
    """Изображении товара"""

    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, verbose_name='Товары')
    # _image = models.FileField('Изображения', upload_to=RandomFileName('products'))
    thumbnail = ProcessedImageField(
        upload_to=RandomFileName('products'),
        processors=[Transpose(), Thumbnail(400)],
        format='WEBP',
    )

    def __str__(self) -> str:
        return self.product.name
    
    class Meta:
        verbose_name = 'Изображения товара'
        verbose_name_plural = 'Изображении товара'


# Main Page models

class Header(models.Model):
    """Карусель для главной страницы"""

    title = models.CharField('Заголовок', max_length=255)
    body = models.CharField('Описание', max_length=255)
    url = models.CharField('Ссылка', max_length=128)
    # image = models.ImageField('Картинка', upload_to=RandomFileName('header_carousel'), blank=False)
    thumbnail = ProcessedImageField(
        upload_to=RandomFileName('header_carousel'),
        processors=[Transpose(), Thumbnail(700)],
        format='WEBP',
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Карусель'
        verbose_name_plural = 'Карусель'



class About(models.Model):
    content = models.TextField('О нас')

    def __str__(self) -> str:
        return f'О нас {self.id}'

    class Meta:
        verbose_name = 'Страница "О нас"'
        verbose_name_plural = 'Страница "О нас"'



class Info(models.Model):
    shipping = models.TextField('Доставка товара')
    payment = models.TextField('Оплата')
    service = models.TextField('Уход')
    qa = models.TextField('Вопросы и ответы')

    def __str__(self) -> str:
        return f'Помощь {self.id}'

    class Meta:
        verbose_name = 'Страница "Помощь"'
        verbose_name_plural = 'Страница "Помощь"'