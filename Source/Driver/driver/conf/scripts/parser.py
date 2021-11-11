import os
import json
from bs4 import BeautifulSoup

import conf.global_settings as settings
import conf.scripts.util as util
import conf.logger as log

DOMAIN = os.environ["URL_DOMAIN"]


def __PARSE__PRODUCT_NAME(parser: BeautifulSoup):
    header__title_wrapper = parser.find("header", class_="title-wrapper")
    span__product_name = header__title_wrapper.find(
        "span", class_="product-name")
    product_name = span__product_name.text.strip().replace('\'', '`')

    return product_name


def __PARSE__PRODUCT_BRAND(parser: BeautifulSoup):
    span__brand_name = parser.find("span", class_="brand-name")
    brand_name = span__brand_name.text.strip().replace('\'', '`')
    a__href = span__brand_name.find("a", href=True)["href"]
    brand_url = DOMAIN + a__href

    return {
        'name': brand_name,
        'url': brand_url.strip().split('javascript:;')[0],
    }


def __PARSE__PRODUCT_PRICE(parser: BeautifulSoup):
    div__product_price_wrapper = parser.find(
        "div", class_="product-price-wrapper")
    try:
        span__price = div__product_price_wrapper.findAll(
            "span", class_="price")
        price = float(span__price[0]["content"])

    except AttributeError:
        price = None

    return price if price != 0.0 else None


def __PARSE__PRODUCT_RATE(parser: BeautifulSoup):
    span__rating_star = parser.find("span", class_="rating-star")
    try:
        rate = span__rating_star.text.strip().replace(',', '.')
    except AttributeError:
        rate = None

    return rate if rate is None else float(rate)


def __PARSE__PRODUCT_IMAGES(parser: BeautifulSoup):
    div__product_details_carousel = parser.find(
        "div", id="productDetailsCarousel")
    picture__itemprop_images = div__product_details_carousel.findAll(
        "picture", itemprop="image")

    images = []
    for picture__itemprop_image in picture__itemprop_images:
        img__ = picture__itemprop_image.find("img")
        try:
            img__src = img__["src"]
        except KeyError:
            img__src = img__["data-src"]

        images.append(img__src)

    return images


def __PARSE__PRODUCT_SUPPLIER(parser: BeautifulSoup):
    div__tab_merchant = parser.find("div", id="tabMerchant")
    table__merchant_list = div__tab_merchant.find("table", id="merchant-list")
    tr__merchant_list_items = table__merchant_list.findAll(
        "tr", class_="merchant-list-item merchant-sort-item")

    merchants = []
    for tr__merchant_list_item in tr__merchant_list_items:
        div__merchant_info = tr__merchant_list_item.find(
            "div", class_="merchant-info")

        # Get rate of supplier
        try:
            a__merchant_rating_top = div__merchant_info.find(
                "a", class_="merchant-rating-top")
            span__merchant_rating = a__merchant_rating_top.find(
                "span", class_="merchant-rating")
            rate = span__merchant_rating.text.strip().replace(',', '.')
        except AttributeError:
            rate = None

        # Get name of supplier
        a__merchant_name = div__merchant_info.find(
            "a", class_="merchant-name", href=True)
        span__merchant_name = a__merchant_name.find("span")
        merchant_name = span__merchant_name.text.strip()

        # Get price of product of supplier
        span__price = tr__merchant_list_item.findAll(
            "span", class_="price")
        price = float(span__price[0].text.split()[
                      0].replace('.', '').replace(',', '.'))

        # Get URL of supplier
        merchant_url = DOMAIN + a__merchant_name["href"]

        merchants.append({
            "name": merchant_name.replace('\'', '`'),
            "rate": rate if rate is None else float(rate),
            "url": merchant_url.strip().split('javascript:;')[0],
            "price": price if price != 0.0 else None,
        })

    return merchants


def __PARSE__PRODUCT_CATEGORY(parser: BeautifulSoup):
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


def __PARSE__PRODUCT_SUBCATEGORY(parser: BeautifulSoup):
    ul__breadcrumbs = parser.find("ul", class_="breadcrumbs")
    li__itemprops = ul__breadcrumbs.findAll(
        "li", itemprop="itemListElement")[2:]

    subcategories = []
    for li__itemprop in li__itemprops:
        a__itemprop = li__itemprop.find("a", itemprop="item", href=True)

        subcategory_name = a__itemprop["title"].strip()
        subcategory_url = a__itemprop["href"].strip()

        subcategories.append({
            "name": subcategory_name,
            "url": subcategory_url.strip().split('javascript:;')[0],
        })

    return subcategories


def parse(url: str, content: str):
    url_hash = util.get_hash(url)
    parser = BeautifulSoup(content, "lxml")

    log.info(url_hash, "is being parsed")

    try:
        product_name = __PARSE__PRODUCT_NAME(parser)
        brand = __PARSE__PRODUCT_BRAND(parser)
        price = __PARSE__PRODUCT_PRICE(parser)
        rate = __PARSE__PRODUCT_RATE(parser)
        images = __PARSE__PRODUCT_IMAGES(parser)
        supplier = __PARSE__PRODUCT_SUPPLIER(parser)
        category = __PARSE__PRODUCT_CATEGORY(parser)
        subcategory = __PARSE__PRODUCT_SUBCATEGORY(parser)
    except Exception as e:
        log.error(url_hash, "is corrupted")
        os.remove(settings.CACHE_FOLDER + url_hash)
        return

    resval = {
        "product name": product_name,
        "url": url.strip().split('javascript:;')[0],
        "brand": brand,
        "price": price,
        "rate": rate,
        "images": images,
        "supplier": supplier,
        "category": category,
        "subcategory": subcategory,
    }

    with open(settings.PRODUCTS_FOLDER + url_hash + '.json', "w+", encoding='utf8') as file:
        json.dump(resval, file, indent=4, ensure_ascii=False)
