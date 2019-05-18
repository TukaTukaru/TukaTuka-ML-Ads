from django import forms
from .models import *

CATEGORY_CHOICE = [
    (1, "Купить вторичное сырье на переработку"),
    (2, "Купить переработанное сырье"),
    (3, "Продать вторичное сырье на переработку"),
    (4, "Продать переработанное сырье"),
]

CATEGORY_RAW = [
        (1, "ПП"),
        (2, "ПНД"),
        (3, "ПВД"),
        (4, "Стрейч"),
        (5, "ПЭТ"),
        (6, "Другое"),

    ]

CATEGORY_GRANULE = [
        (1, "Гранула ПП"),
        (2, "Гранула ПНД"),
        (3, "Гранула ПВД"),
        (4, "Гранула стрейч"),
        (5, "Другое"),

    ]

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['full_name', 'phone_number', 'company_name', 'company_adress', 'email', 'site', ]


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        category = forms.ChoiceField(choices=CATEGORY_CHOICE, widget=forms.RadioSelect())
        category1 = forms.ChoiceField(choices=CATEGORY_RAW, widget=forms.RadioSelect())

        fields = ['author', 'category','title', 'description' , 'category1', 'price', 'volume', 'photo']

