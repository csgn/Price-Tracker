import os
import dotenv

import conf.global_settings as settings

if __name__ == "__main__":
    """ SET DATABASE CONFIG """
    dotenv.load_dotenv('./resources/.env')

    if not os.path.exists(settings.CACHE_FOLDER):
        os.makedirs(settings.CACHE_FOLDER)

    if not os.path.exists(settings.PRODUCTS_FOLDER):
        os.makedirs(settings.PRODUCTS_FOLDER)

    __import__("tracker").main()
