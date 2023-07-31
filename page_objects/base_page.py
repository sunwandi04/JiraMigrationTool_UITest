import allure
from playwright.sync_api import Page, Error


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step('Click locator - {locator}')
    def click(self, locator: str):
        self.page.locator(locator).click()

    @allure.step('Click text - {text}')
    def click_by_text(self, text: str):
        self.page.get_by_text(text).click()

    @allure.step('select option - {text} - {title}')
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

    @allure.step('Click tooltip - {tooltip}')
    def click_by_tooltip(self, tooltip: str, text: str):
        self.page.get_by_role("tooltip", name=tooltip).get_by_text(text).click()

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
        self.page.get_by_label(label).fill(" ")
        self.page.get_by_label(label).fill(text)

    @allure.step('Type text - {text} into placeholder - {placeholder}')
    def type(self, placeholder: str, text: str):
        self.page.get_by_placeholder(placeholder).click()
        self.page.get_by_placeholder(placeholder).fill(" ")
        self.page.get_by_placeholder(placeholder).fill(text)

    @allure.step('expand or fold text - {text} ')
    def expand_fold(self, text: str):
        self.page.get_by_role("cell", name=text).get_by_role("img").click()

    @allure.step('Click textbox - {textbox}')
    def click_by_textbox(self, textbox: str, text: str):
        self.page.get_by_role("textbox", name=textbox).fill(text)

    def visible(self, locator, wait_time=15, idx=1):

        el = self.page.locator(locator)

        try:
            el.wait_for(timeout=wait_time * 1000)
            # not found
        except TimeoutError as e:
                print(f'\nNot found: {e}')
                return None, False

        # multiple el found
        except Error as ee:
                # assert el.count() > 1, 'Expect multi elements'
                if el.count() > 1:
                    print(f"\n{'=' * 18} Multiple elements found{'=' * 18}\n{ee}")
                    curr = el.nth(idx - 1)
                    v = curr.is_visible()
                    return curr, v
                else:
                    return None, False

        if el.is_visible():
            return el, True
        else:
            return el, False

    def contains(self, text: str, el_type='text'):
        _postfix = {
            'text': '',
            'input': 'input',
            'textarea': 'textarea',
            'dropdown': 'dropdown',
            'div': 'div',
            'table_cell': 'table_cell',
        }
        _pf = _postfix.get(el_type, '')
        my_path = f'//*[contains(text(), "{text}")]'
        if _pf:
            my_path = my_path + f'/following-sibling::*//{_pf}'

        v = self.visible(my_path)
        if not v[1]:
            # self._attach(my_path)
            print(f'ElementNotFound: {text}')
            raise AssertionError('ElementNotFound')

        return v

    def element_is_exist(self, locator, is_exist=True, wait_time=30):
        """
        断言页面是否存在元素
        :param wait_time:
        :param locator: 定位
        :param is_exist: 断言 True or False
        :return:
        """
        element, is_v = self.visible(locator, wait_time=wait_time)
        assert is_v == is_exist, AssertionError('AssertionError')

    def attach(self):
        ...
        # self.page.screenshot(path=)