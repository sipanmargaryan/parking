from django.db import models
from django.db.models import F

__all__ = (
    'Country',
    'Brand',
    'CarModel',
    'Color',
)


class Country(models.Model):
    name = models.CharField(max_length=256, unique=True)
    flag = models.ImageField(upload_to='images/flags')
    country_code = models.CharField(max_length=8, unique=True)
    country_phone_code = models.CharField(max_length=8)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        verbose_name_plural = 'Car Brands'

    def __str__(self):
        return self.name

    @classmethod
    def as_choices(cls):
        return cls.objects.values_list('pk', 'name')


class CarModel(models.Model):
    name = models.CharField(max_length=256)
    make = models.ForeignKey(Brand, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Car Models'
        unique_together = (('name', 'make', ), )

    def __str__(self):
        return self.name

    @classmethod
    def as_choices(cls):
        return cls.objects.values_list('pk', 'name')

    @classmethod
    def as_choices_with_makes(cls):
        return cls.objects.annotate(make_pk=F('make__pk')).values('pk', 'name', 'make_pk'),


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color_code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    @classmethod
    def as_choices(cls):
        return cls.objects.values_list('pk', 'name', 'color_code')

