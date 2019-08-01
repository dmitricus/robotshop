from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя категории', max_length=128, unique=True)
    description = models.TextField(verbose_name='описание категории', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категоря'
        verbose_name_plural = 'Категория'


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='имя товара', max_length=128, unique=True)
    image = models.ImageField(upload_to='product_images', blank=True)
    shot_desc = models.CharField(verbose_name='краткое описание товара', max_length=60, blank=True)
    description = models.TextField(verbose_name='описание товара', blank=True)
    price = models.DecimalField(verbose_name='цена товара', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='количество на складе', default=0)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.category.name)


    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товар'

