from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from django.conf import settings


# Create your models here.


class Company(models.Model):
    full_name = models.CharField(max_length=200)
    phone_number = PhoneNumberField(unique=True)
    company_name = models.CharField(blank=True, null=True, max_length=200, db_index=True)
    company_adress = models.CharField(max_length=200, db_index=True)
    email = models.EmailField(blank=True, null=True, unique=True, db_index=True)
    site = models.URLField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.phone_number)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Ad(models.Model):
    CATEGORY_CHOICE = (
        (1, "Купить вторичное сырье на переработку"),
        (2, "Купить переработанное сырье"),
        (3, "Продать вторичное сырье на переработку"),
        (4, "Продать переработанное сырье"),
    )

    CATEGORY_RAW = (
        (1, "ПП"),
        (2, "ПНД"),
        (3, "ПВД"),
        (4, "Стрейч"),
        (5, "ПЭТ"),
        (6, "Другое"),

    )

    CATEGORY_GRANULE = (
        (1, "Гранула ПП"),
        (2, "Гранула ПНД"),
        (3, "Гранула ПВД"),
        (4, "Гранула стрейч"),
        (5, "Другое"),

    )

    price = models.PositiveIntegerField(blank=True, null=True)
    volume = models.PositiveIntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to='prod_img', blank=True, verbose_name='Фото продукции')

    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    author = models.ForeignKey(
        on_delete=models.CASCADE, to=Company)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.IntegerField(choices=CATEGORY_CHOICE, default=0)
    category1 = models.IntegerField(choices=CATEGORY_RAW, default=0, blank=True, null=True)
    category2 = models.IntegerField(choices=CATEGORY_GRANULE, default=0, blank=True, null=True)

    def __str__(self):
        return "дата: {}".format(self.created_at)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Mail(models.Model):
    email = models.EmailField(unique=True, db_index=True)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'email'
        verbose_name_plural = 'emails'
