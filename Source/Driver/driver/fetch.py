from tqdm import tqdm
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


DOMAIN = 'https://www.hepsiburada.com'

def GET__PRODUCT_NAME(parser):
    header__title_wrapper = parser.find("header", class_="title-wrapper")
    span__product_name = header__title_wrapper.find("span", class_="product-name")
    product_name = span__product_name.text.strip()

    return product_name

   
def GET__PRODUCT_BRAND(parser):
    span__brand_name = parser.find("span", class_="brand-name")
    brand_name = span__brand_name.text.strip()
    a__href = span__brand_name.find("a", href=True)["href"]
    brand_url = DOMAIN + a__href

    return {
        'name': brand_name,
        'url': brand_url,
    }


def GET__PRODUCT_PRICE(parser):
    div__product_price_wrapper = parser.find("div", class_="product-price-wrapper")
    try:
        span__price = div__product_price_wrapper.find("span", class_="price")
        price = span__price.text.split()
    except AttributeError:
        price = None

    return price


def GET__PRODUCT_RATE(parser):
    span__rating_star = parser.find("span", class_="rating-star")
    try:
        rate = span__rating_star.text.strip().replace(',', '.')
    except AttributeError:
        rate = None

    return rate


def GET__PRODUCT_IMAGES(parser):
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

def GET__PRODUCT_SUPPLIER(parser):
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
            rating = span__merchant_rating.text.strip().replace(',', '.')
        except AttributeError:
            rating = None

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
            "rating": rating,
            "url": merchant_url,
            "price": price,
        })

    return merchants


URLs = [
    "https://www.hepsiburada.com/xiaomi-mi-robot-vacuum-mop-pro-siyah-akilli-robot-supurge-p-HBV00000SDB4D",
    "https://www.hepsiburada.com/lenovo-v14-g2-itl-intel-core-i5-1135g7-8-gb-256gb-ssd-14-full-hd-freedos-tasinabilir-bilgisayar-82ka0025tx-p-HBCV00000R3940",
    "https://www.hepsiburada.com/oppo-reno-5-lite-128-gb-oppo-turkiye-garantili-p-HBCV0000051OFU?magaza=Hepsiburada",
    "https://www.hepsiburada.com/bilinmeyen-bir-kadinin-mektubu-stefan-zweig-p-kisbank06604",
    "https://www.hepsiburada.com/oral-b-expert-precision-clean-pilli-dis-fircasi-p-SGBRAUNDB04EXP?magaza=Hepsiburada",
    "https://www.hepsiburada.com/apple-airpods-3-nesil-kulaklik-mme73tu-a-p-HBCV00000U44QM",
    "https://www.hepsiburada.com/vestel-50ua9600-50-126-ekran-uydu-alicili-4k-ultra-hd-android-smart-led-tv-p-HBV00000Y2TH1?magaza=Hepsiburada",
    "https://www.hepsiburada.com/electronic-arts-fifa-22-ps4-turkce-menu-p-HBCV00000QRJMO?magaza=Hepsiburada",
    "https://www.hepsiburada.com/grundig-gdh-80-y-8-kg-16-programli-isi-pompali-kurutma-makinesi-p-MTGRUGDH80?magaza=Grundig%20T%C3%BCrkiye",
    "https://www.hepsiburada.com/okuma-aria-65-olta-makinesi-p-hbcv00000j9dz1",
    "https://www.hepsiburada.com/develi-celik-yemek-bicak-6li-p-hbv000008qtoa",
    "https://www.hepsiburada.com/amazfit-t-rex-pro-black-akilli-saat-p-hbcv000004j6qk",
    "https://www.hepsiburada.com/logitech-g-g300s-2-500-dpi-optik-kablolu-oyuncu-mouse-siyah-p-bd802935",
    "https://www.hepsiburada.com/grundig-bl-4781-rendeli-700-watt-el-blender-seti-p-hbv00000l8001",
    "https://www.hepsiburada.com/ariel-12-kg-toz-camasir-deterjani-dag-esintisi-renkiler-icin-p-hbv00000vf28o",
]

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=*")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver


def worker(url):
    driver.get(url)
    content = driver.page_source
    parser = BeautifulSoup(content, "lxml")

    product_name = GET__PRODUCT_NAME(parser)
    brand = GET__PRODUCT_BRAND(parser)
    price = GET__PRODUCT_PRICE(parser)
    rate = GET__PRODUCT_RATE(parser)
    images = GET__PRODUCT_IMAGES(parser)
    supplier = GET__PRODUCT_SUPPLIER(parser)

    print(product_name, brand, price, rate, images, supplier, sep="\n")


driver = get_driver()

for url in tqdm(URLs):
    worker(url)

driver.quit()
