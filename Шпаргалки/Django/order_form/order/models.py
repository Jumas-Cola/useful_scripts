from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Order(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    mechanism = models.ForeignKey('Mechanism', on_delete=models.CASCADE)
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    address = models.TextField(
        help_text='Адрес клиента',
        verbose_name='Адрес'
    )
    contacts = models.TextField(
        help_text='Контактные данные клиента',
        verbose_name='Контакты'
    )

    def get_absolute_url(self):
        return reverse('order_detail', args=[str(self.id)])


class Material(models.Model):
    name = models.CharField(
        max_length=1000,
        help_text='Название материала',
        verbose_name='Материал'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
    )

    def __str__(self):
        return self.name


class Mechanism(models.Model):
    name = models.CharField(
        max_length=1000,
        help_text='Название механизма',
        verbose_name='Механизм'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
    )

    def __str__(self):
        return self.name
