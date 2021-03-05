from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.quotes_page import QuotesPage, InvalidTagForAuthorError

URL_TO_SCRAPE = "http://quotes.toscrape.com/search.aspx"
PATH_TO_CHROME = "/usr/local/bin/chromedriver"


def create_browser(url: str) -> webdriver.Chrome:
    chr_options = Options()
    chr_options.add_experimental_option("detach", True)
    chrome = webdriver.Chrome(executable_path=PATH_TO_CHROME, options=chr_options)

    chrome.get(url)
    return chrome


def app():
    try:
        chrome = create_browser(URL_TO_SCRAPE)
        page = QuotesPage(chrome)

        author_name = input("Enter the author would you'd like quotes from: ")
        selected_tag = input("Select a tag: ")

        page.search_for_quotes(author_name, selected_tag)
        print(page.quotes)
    except InvalidTagForAuthorError as e:
        print(e)
    except Exception as e:
        print(e)
        print("An unknown error occurred.")


if __name__ == "__main__":
    app()
