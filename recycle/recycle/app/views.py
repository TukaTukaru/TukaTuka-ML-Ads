import datetime
from django.views.decorators.http import require_http_methods,require_GET,require_POST
from django.shortcuts import render, get_object_or_404
from .models import Ad, Company

# Create your views here.
# маршрутизация, логика работы приложения
from django.http import HttpResponse
import logging


def index(request):
    return HttpResponse("Hello, {}".format(request.user))

@require_GET
def get_company(request):
    phone_number_ = "+79671234561"

    company = get_object_or_404(Company, phone_number=phone_number_)
    return HttpResponse("<p>компания: {}</p> "
                        "<p>Владелец: {}</p> "
                        "<p>номер телефона: {}</p>".format(company.company_name,
                                                           company.full_name,
                                                           company.phone_number
                                                           ))

@require_POST
def post_company(request):
    full_name_ = "Игуанов Игуан Игуанович"
    phone_number_ = "+79671234561"
    company_name_ = "вторСырье"
    company_adress_ = "Москва"

    # if Company.objects.get(phone_number__exact=phone_number_) is not None:
    company = Company(full_name=full_name_, phone_number=phone_number_, company_name=company_name_,
                      company_adress=company_adress_)
    company.save()
    return HttpResponse("<p>компания по переработке сырья добавлена: </p>"
                        "<p>название компании: {}</p>"
                        "<p>представитель: {}</p>"
                        "<p>контактный номер: {}</p>"
                        "<p>еmail: {}</p>"
                        "<p>адрес компании: {}</p>"
                        "<p>веб-сайт: {}</p>".format(company.company_name,
                                                     company.full_name,
                                                     company.phone_number,
                                                     company.email,
                                                     company.company_adress,
                                                     company.site))

@require_http_methods(["PATCH"])
def patch_company(request):
    phone_number_ = "+79671234561"
    site_ = "www.iguan1.ru"
    company = get_object_or_404(Company, phone_number__exact=phone_number_)
    Company.objects.filter(phone_number__exact=phone_number_).update(site=site_)
    return HttpResponse("в компанию добавлен сайт: {}".format(site_))

@require_http_methods(["DELETE"])
def del_company(request):
    phone_number_ = "+79671234561"
    company = get_object_or_404(Company, phone_number__exact=phone_number_)
    company.delete()
    return HttpResponse("компания с номером: {} удалена".format(phone_number_))
