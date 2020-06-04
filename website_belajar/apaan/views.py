from django.shortcuts import render
import requests
from urllib.parse import quote_plus
from urllib.parse import urljoin
from requests.utils import requote_uri
from requests_html import HTMLSession, AsyncHTMLSession

from bs4 import BeautifulSoup
from . import models
from urllib.parse import urlsplit
from lxml import html, etree
import html5lib
import re

import html5lib

from python_anticaptcha import AnticaptchaClient, ImageToTextTask
PARENT_URL2 ='https://www.rumah123.com/'
BASE_URL = 'https://www.lamudi.co.id/buy/?q={}'
BASE_URL2 = 'https://www.rumah123.com/en/sale/all-residential/?q={}'

# Create your views here.
def home_request(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_URL.format(quote_plus(search))
    final_url2 = BASE_URL2.format(requote_uri(search))
    print(final_url)
    print(final_url2)

    response = requests.get(final_url)
    headers = requests.utils.default_headers()
    headers.update({'user-agent': 'GoogleChrome'})

    response2 = requests.get(final_url2.replace(u'\ufeff', ''))

    headers = requests.utils.default_headers()
    headers.update({'user-agent': 'GoogleChrome'})


    session = HTMLSession()
    resp = session.get(final_url2)
    print(resp)
    soup4 = BeautifulSoup(resp.html.html, "lxml")
    #image = soup4.find_all(class_ = 'BaseCardstyle__ListingPosterMainWrapper-LdsSD KSRNa' )
    image2 = soup4.find_all(class_= 'img-wrapper')
    for gambar in image2:
        link_gambar = gambar.find(class_ = 'Rumah Cimanggis Pinggir Jalan Dekat Pintu Tol di Depok, Cimanggis, Depok 1')
        print(link_gambar)





    final_post = []
    final_post2 = []
    print(final_post2)


    data = response.text
    soup = BeautifulSoup(data, features='lxml')
    post_listing = soup.find_all(class_='card ListingCell-content js-MainListings-container ListingCell-wrapper')

    data2 = response2.text

    soup2 = BeautifulSoup(data2,features='lxml')
    post_listing2 = soup2.find_all(class_= 'BaseCardstyle__ListingContainer-pryVa gCOzDl')










    print('*' * 100)

    for post in post_listing:
        post_title = post.find(class_='ListingCell-KeyInfo-title').text
        post_title2 = post_title.strip()


        post_link = post.find('a').get('href')

        if post.find(class_='PriceSection-FirstPrice'):
            post_price = post.find(class_='PriceSection-FirstPrice').text
        else:
            post_price = 'N/A'

        if post.find(class_='ListingCell-image'):
            post_image_id = post.find(class_='ListingCell-image').img['data-src']
            #post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_id = 'https://craigslist.org/images/peace.jpg'

        final_post.append((post_title2, post_price, post_link, post_image_id))

    #part rumah123.com

    for postrumah123 in post_listing2:
        post_titlerumah123 = postrumah123.find(class_='BaseCardstyle__ListingTitleWrapper-bFjnJr hTMjgq')
        if post_titlerumah123 is not None:
            post_titlerumah123 = post_titlerumah123.text
        else:
            post_titlerumah123 = 'rumah dijual di daerah strategis'


        post_linkrumah123 = postrumah123.find('a').get('href')

        if '.com' not in post_linkrumah123:
            post_linkrumah123_revisi = urljoin(PARENT_URL2, post_linkrumah123)
        else:
            post_linkrumah123_revisi = post_linkrumah123


        if postrumah123.find(class_='listing-primary-price ListingPrice__Wrapper-FYsEL cpaEEX'):
            post_pricerumah123 = postrumah123.find(class_='listing-primary-price-item ListingPrice__ItemWrapper-egelzL fnIFZc').get_text()
        else:
            post_price = 'N/A'


        final_post2.append((post_titlerumah123, post_pricerumah123, post_linkrumah123_revisi,))

        #else:
         #   post_image_idrumah123 = 'https://craigslist.org/images/peace.jpg'














        #print(post_pricerumah123)



        #final_post2.append((post_titlerumah123_2, post_pricerumah123, post_linkrumah123))


    for_frontend = {
        'search': search,
        'final_post': final_post,
        'final_post2': final_post2



    }

    return render(request, 'apaan/new_search.html', for_frontend)
