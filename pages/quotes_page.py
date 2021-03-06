from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from locators.quote_page_locators import QuotesPageLocators
from parsers.quote import QuoteParser


class QuotesPage(object):
    """
    Searches within HTML page using quote selector to
    return list of QuoteParser objects
    """

    def __init__(self, browser):
        self.browser = browser

    @property
    def quotes(self) -> List[QuoteParser]:
        locator = QuotesPageLocators.QUOTE
        quote_tags = self.browser.find_elements_by_css_selector(locator)
        return [QuoteParser(elem) for elem in quote_tags]

    @property
    def author_dropdown(self) -> Select:
        element = self.browser.find_element_by_css_selector(QuotesPageLocators.AUTHOR_DROPDOWN)
        return Select(element)

    def select_author(self, author: str):
        self.author_dropdown.select_by_visible_text(author)

    @property
    def tag_dropdown(self) -> Select:
        element = self.browser.find_element_by_css_selector(QuotesPageLocators.TAGS_DROPDOWN)
        return Select(element)

    def select_tag(self, tag: str):
        self.tag_dropdown.select_by_visible_text(tag)

    def get_available_tags(self) -> List[str]:
        return [option.text.strip() for option in self.tag_dropdown.options]

    @property
    def search_button(self):
        element = self.browser.find_element_by_css_selector(QuotesPageLocators.SEARCH_BUTTON)
        return element

    def search_for_quotes(self, author_name: str, selected_tag: str) -> List[QuoteParser]:
        self.select_author(author_name)

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, QuotesPageLocators.DROPDOWN_VALUE_OPTION)
            )
        )
        try:
            self.select_tag(selected_tag)
        except NoSuchElementException:
            raise InvalidTagForAuthorError(
                f"Author `{author_name}` does not have any questions tagged with {selected_tag}."
            )
        self.search_button.click()


class InvalidTagForAuthorError(ValueError):
    pass
