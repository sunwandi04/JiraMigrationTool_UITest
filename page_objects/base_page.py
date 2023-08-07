import allure, os
from playwright.sync_api import Page, Error
from falcons.com.env import RuntimeVars
from falcons.helper import mocks
from falcons.com.nick import (
    step,
    attachment_type,
    attach,
)
import logging


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

    def attach(self, png):
        """
        截图功能
        :param png: 截图文件名称
        :return:
        """
        base_path = RuntimeVars.tmp_files
        p = f'{png}-{mocks.ones_uuid()}'
        s_path = os.path.join(base_path, f'{p}.png')
        allure.attach(self.page.screenshot(path=s_path, full_page=True), p, attachment_type.PNG)


class LoggerHandler:
    # 初始化 Logger
    def __init__(self,
                 name='root',
                 logger_level='DEBUG',
                 file=None,
                 logger_format='%(asctime)s-%(message)s'
                 # logger_format = '%(asctime)s-%(filename)s-%(lineno)d-%(message)s'
                 ):
        # 1、初始化logger收集器
        logger = logging.getLogger(name)

        # 2、设置日志收集器level级别
        logger.setLevel(logger_level)

        # 5、初始化 handler 格式
        fmt = logging.Formatter(logger_format)

        # 3、初始化日志处理器

        # 如果传递了文件，就会输出到file文件中
        if file:
            file_handler = logging.FileHandler(file)
            # 4、设置 file_handler 级别
            file_handler.setLevel(logger_level)
            # 6、设置handler格式
            file_handler.setFormatter(fmt)
            # 7、添加handler
            logger.addHandler(file_handler)

        # 默认都输出到控制台
        stream_handler = logging.StreamHandler()
        # 4、设置 stream_handler 级别
        stream_handler.setLevel(logger_level)
        # 6、设置handler格式
        stream_handler.setFormatter(fmt)
        # 7、添加handler
        logger.addHandler(stream_handler)

        # 设置成实例属性
        self.logger = logger

    # 返回日志信息

    def debug(self, msg):
        return self.logger.debug(msg)

    def info(self, msg):
        return self.logger.info(msg)

    def warning(self, msg):
        return self.logger.warning(msg)

    def error(self, msg):
        return self.logger.error(msg)

    def critical(self, msg):
        return self.logger.critical(msg)
