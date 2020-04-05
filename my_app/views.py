import requests

from . import models
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from bs4.element import Tag


BASE_CRAIGSLIST_URL = 'https://manila.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_listings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        post_price = post.find(class_='result-price').text if post.find(class_='result-price') else 'N/A'

        if post.find('a').get('data-ids'):
            post_image_id = post.find('a').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://manila.craigslist.org/images/peace.jpg'

        final_listings.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_listings': final_listings
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)

