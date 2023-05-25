import dotenv

from page_objects.base_page import BasePage


# 自己定于了一个类，继承了BasePage
class FrontPage(BasePage):

    def guide_page(self):
        with self.page.expect_popup() as popup_info:
            self.click_by_button("查看使用指南")
        popup = popup_info.value
        return popup

    def start_migration(self):
        self.click_by_button("开始迁移")

    def start_assess(self):
        self.click_by_button("开始评估")

    def agree_terms(self, locator=''):
        self.check(locator)
        self.click_by_button('确定')

    def dont_agree_terms(self, locator=''):
        self.check(locator)
        self.uncheck(locator)
        self.click_by_button('确定')

    def change_language(self):
        self.click_by_button('简体中文')
        self.click_by_text('English')
        self.page.wait_for_load_state()
        self.click_by_button('English')
        self.click_by_text('日本語')
        self.page.wait_for_load_state()
        self.click_by_button('日本語')
        self.click_by_text('简体中文')
