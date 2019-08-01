from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mainapp.models import Product, ProductCategory
from basketapp.models import Basket
import os, json
import random

def loadFromJSON(file_name):
    root = os.path.dirname(__file__)
    JSON_PATH = root + '/json'
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)

def getBasket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []

def getHotProduct():
    products = Product.objects.filter(is_active=True)
    return random.sample(list(products), 1)[0]

def getSameProducts(hot_product):
    same_products = Product.objects.filter(category=hot_product.category, is_active=True).exclude(pk=hot_product.pk)[:4]
    return same_products

# Create your views here.
def main(request):
    title = 'Главная'
    catalog_list = Product.objects.filter(is_active=True)[:6]
    preview_list = Product.objects.filter(is_active=True)[:4]
    products = Product.objects.filter(is_active=True)[:3]
    basket = getBasket(request.user)


    main_slider_list = loadFromJSON("main_slider")
    top_slider_list = loadFromJSON("top_slider")

    hot_product = getHotProduct()
    same_products = getSameProducts(hot_product)

    content = {
        'title': title,
        'catalog_list': catalog_list,
        'preview_list': preview_list,
        'products': products,
        'main_slider_list': main_slider_list,
        'top_slider_list': top_slider_list,
        'basket': basket,
        'hot_product': hot_product,
        'same_products': same_products,
    }

    return render(request, 'mainapp/index.html', content)


def catalog(request, pk=None, page=1):
    print('пришел pk категории {}'.format(pk))

    title = 'продукты'
    category_list = ProductCategory.objects.filter(is_active=True)
    basket = getBasket(request.user)

    if pk:
        if pk != '0':
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('-price')
        else:
            category = {
                'pk': 0,
                'name': 'все',
            }
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('-price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'category_list': category_list,
            'category': category,
            'products': products_paginator,
            'basket': basket,
        }

        return render(request, 'mainapp/catalog.html', content)

    content = {
        'title': title,
        'category_list': category_list,
        'basket': basket,
    }

    return render(request, 'mainapp/catalog.html', content)

def contacts(request):

    title = 'Контакты'
    basket = getBasket(request.user)
    contact_list = loadFromJSON("contact_list")

    content = {
        'title': title,
        'contact_list': contact_list,
        'basket': basket,
    }

    return render(request, 'mainapp/contacts.html', content)

def product(request, pk=None):
    category = ProductCategory.objects.filter(is_active=True)
    if pk == None:
        product = Product.objects.objects.first()
    else:
        product = Product.objects.filter(pk=pk)

    basket = getBasket(request.user)
    catalog = Product.objects.filter(is_active=True)[:6]

    content = {
        'catalog_list': catalog,
        'product_list': product,
        'category_list': category,
        'basket': basket,
    }

    return render(request, 'mainapp/product.html', content)