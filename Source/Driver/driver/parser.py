import os
from bs4 import BeautifulSoup

DOMAIN = 'https://www.hepsiburada.com'

def PARSE__PRODUCT_NAME(parser: BeautifulSoup):
    header__title_wrapper = parser.find("header", class_="title-wrapper")
    span__product_name = header__title_wrapper.find("span", class_="product-name")
    product_name = span__product_name.text.strip()

    return product_name

   
def PARSE__PRODUCT_BRAND(parser: BeautifulSoup):
    span__brand_name = parser.find("span", class_="brand-name")
    brand_name = span__brand_name.text.strip()
    a__href = span__brand_name.find("a", href=True)["href"]
    brand_url = DOMAIN + a__href

    return {
        'name': brand_name,
        'url': brand_url,
    }


def PARSE__PRODUCT_PRICE(parser: BeautifulSoup):
    div__product_price_wrapper = parser.find("div", class_="product-price-wrapper")
    try:
        span__price = div__product_price_wrapper.find("span", class_="price")
        price = span__price.text.split()
    except AttributeError:
        price = None

    return price


def PARSE__PRODUCT_RATE(parser: BeautifulSoup):
    span__rating_star = parser.find("span", class_="rating-star")
    try:
        rate = span__rating_star.text.strip().replace(',', '.')
    except AttributeError:
        rate = None

    return rate


def PARSE__PRODUCT_IMAGES(parser: BeautifulSoup):
    div__product_details_carousel = parser.find("div", id="productDetailsCarousel")
    picture__itemprop_images = div__product_details_carousel.findAll("picture", itemprop="image")

    images = []
    for picture__itemprop_image in picture__itemprop_images:
        img__ = picture__itemprop_image.find("img")
        try:
            img__src = img__["src"]
        except KeyError:
            img__src = img__["data-src"]

        images.append(img__src)

    return images

def PARSE__PRODUCT_SUPPLIER(parser: BeautifulSoup):
    div__tab_merchant = parser.find("div", id="tabMerchant")
    table__merchant_list = div__tab_merchant.find("table", id="merchant-list")
    tr__merchant_list_items = table__merchant_list.findAll("tr", class_="merchant-list-item merchant-sort-item")

    merchants = []
    for tr__merchant_list_item in tr__merchant_list_items:
        div__merchant_info = tr__merchant_list_item.find("div", class_="merchant-info")

        # Get rate of supplier
        try:
            a__merchant_rating_top = div__merchant_info.find("a", class_="merchant-rating-top")
            span__merchant_rating = a__merchant_rating_top.find("span", class_="merchant-rating")
            rate = span__merchant_rating.text.strip().replace(',', '.')
        except AttributeError:
            rate = None

        # Get name of supplier
        a__merchant_name = div__merchant_info.find("a", class_="merchant-name", href=True)
        span__merchant_name = a__merchant_name.find("span")
        merchant_name = span__merchant_name.text.strip()
        
        # Get price of product of supplier
        span__price_value = tr__merchant_list_item.find("span", class_="price")
        price = span__price_value.text.strip().split()
        
        # Get URL of supplier
        merchant_url = DOMAIN + a__merchant_name["href"]

        merchants.append({
            "name": merchant_name,
            "rate": rate,
            "url": merchant_url,
            "price": price,
        })

    return merchants


def PARSE__PRODUCT_CATEGORY(parser: BeautifulSoup):
    ul__breadcrumbs = parser.find("ul", class_="breadcrumbs")
    li__itemprop = ul__breadcrumbs.findAll("li", itemprop="itemListElement")[1]
    a__itemprop = li__itemprop.find("a", itemprop="item", href=True)

    category_name = a__itemprop["title"].strip()
    category_url = a__itemprop["href"].strip()

    category = {
        "name": category_name,
        "url": category_url,
    }

    return category


def PARSE__PRODUCT_SUBCATEGORY(parser: BeautifulSoup):
    ul__breadcrumbs = parser.find("ul", class_="breadcrumbs")
    li__itemprops = ul__breadcrumbs.findAll("li", itemprop="itemListElement")[2:]

    subcategories = []
    for li__itemprop in li__itemprops:
        a__itemprop = li__itemprop.find("a", itemprop="item", href=True)

        subcategory_name = a__itemprop["title"].strip()
        subcategory_url = a__itemprop["href"].strip()

        subcategories.append({
            "name": subcategory_name,
            "url": subcategory_url,
        })

    return subcategories
