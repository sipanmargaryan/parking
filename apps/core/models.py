from django.contrib.auth import get_user_model
from django.db import models

class BaseCategory(models.Model):
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    @classmethod
    def as_choices(cls):
        return cls.objects.values_list('pk', 'name')


class Country(models.Model):
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class Brand(BaseCategory):
    class Meta:
        verbose_name_plural = 'Car Makes'


class CarModelCategory(models.Model):
    name = models.CharField(max_length=256)
    # make = models.ForeignKey(CarMakeCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Car Models'
        # unique_together = (('name', 'make', ), )

    def __str__(self):
        return self.name

    @classmethod
    def as_choices(cls):
        return cls.objects.values_list('pk', 'name')


class Car(models.Model):
    pass