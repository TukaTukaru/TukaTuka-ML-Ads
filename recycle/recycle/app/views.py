import datetime
from django.views.decorators.http import require_http_methods,require_GET,require_POST
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ad, Company
from django.contrib.auth.decorators import login_required
import pdb
from .forms import *
from django.forms.models import model_to_dict

# Create your views here.
# маршрутизация, логика работы приложения
from django.http import HttpResponse
import logging


def main(request):
    return HttpResponse("Hello, {}".format(request.user))

@login_required
def post_company(request):
    form = CompanyForm(request.POST or None)
    if form.is_valid():
        print("if form.is_valid")
        company_form = form.save()
    return render(request, 'post_company.html', context={'form': form})

@login_required
def change_company(request,company_name):
    company = get_object_or_404(Company, company_name=company_name)
    form = CompanyForm(request.POST or None, initial=model_to_dict(company), instance=company,)
    if form.is_valid():
        print("if form.is_valid")
        company_form = form.save()
    return render(request, 'change_company.html', context={'form': form})

@login_required
def get_company(request,company_name):
    company = get_object_or_404(Company, company_name=company_name)
    return render(request,'get_company.html', context={'form': company})

@login_required
def del_company(request, company_name):
    company = get_object_or_404(Company, company_name=company_name)
    full_name = company.full_name
    phone_number = company.phone_number
    adress = company.company_adress
    email = company.email
    site = company.site
    company.delete()
    return render(request, 'del_company.html', context={'full_name':full_name,
                                                        'phone_number':phone_number,
                                                        'adress':adress,
                                                        'email':email,
                                                        'site':site,
                                                        'company_name':company_name})

@login_required
def post_ad(request):
    form = AdForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request,'post_ad.html', context={'form': form})

@login_required
def get_ad(request,title):
    ad = get_object_or_404(Ad, title=title)
    return render(request,'get_ad.html', context={'form': ad})

