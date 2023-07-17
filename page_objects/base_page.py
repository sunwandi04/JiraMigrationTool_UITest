import allure
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step('Click locator - {locator}')
    def click(self, locator: str):
        self.page.locator(locator).click()

    @allure.step('Click text - {text}')
    def click_by_text(self, text: str):
        self.page.get_by_text(text).click()

    @allure.step('select option - {text}-{title}')
    def select_option(self, title: str, text: str):
        self.page.get_by_title(title).get_by_text(text).click()

    @allure.step('Click button - {button}')
    def click_by_button(self, button: str):
        self.page.get_by_role("button", name=button).click()

    @allure.step('Click button - {button}')
    def click_by_dialog_button(self, button: str):
        self.page.get_by_role("dialog").get_by_role("button", name=button).click()

    @allure.step('Click link - {link}')
    def click_by_link(self, link: str):
        self.page.get_by_role("link", name=link).click()

    @allure.step('Click label - {label}')
    def click_by_label(self, label: str):
        self.page.get_by_label(label).click()

    @allure.step('Click title - {title}')
    def click_by_title(self, title: str):
        self.page.get_by_title(title).click()

    @allure.step('Click dropbox - {dropbox}')
    def click_dropbox(self, name: str, dropbox: str):
        self.page.get_by_role("row", name=name).get_by_text(dropbox).click()

    @allure.step('Check checkbox')
    def check(self, locator: str):
        self.page.get_by_label(text=locator, exact=True).check()

    @allure.step('Uncheck checkbox')
    def uncheck(self, locator: str):
        self.page.get_by_label(text=locator, exact=True).uncheck()

    @allure.step('Hover locator - {locator}')
    def hover(self, locator: str):
        self.page.locator(locator).hover()

    @allure.step('Input text - {text} into label - {label}')
    def input(self, label: str, text: str):
        self.page.get_by_label(label).click()
        self.page.get_by_label(label).fill(text)

    @allure.step('Type text - {text} into placeholder - {placeholder}')
    def type(self, placeholder: str, text: str):
        self.page.get_by_placeholder(placeholder).click()
        self.page.get_by_placeholder(placeholder).fill(text)

    @allure.step('expand or fold text - {text} ')
    def expand_fold(self, text: str):
        self.page.get_by_role("cell", name=text).get_by_role("img").click()
