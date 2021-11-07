import dotenv

if __name__ == "__main__":
    """ SET DATABASE CONFIG """
    dotenv.load_dotenv('./resources/.env')

    __import__("tracker").main()
