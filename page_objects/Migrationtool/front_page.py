import re
from JiraMigrationTool_UITest.page_objects.base_page import BasePage


class FrontPage(BasePage):

    def guide_page(self):
        with self.page.expect_popup() as popup_info:
            self.click_by_button("查看使用指南")
        popup = popup_info.value
        return popup

    def download_file(self):
        with self.page.expect_download() as download_info:
            self.click_by_text("下载 Jira 数据迁移清单")
        download_info = download_info.value
        return download_info

    def help_doc(self):
        with self.page.expect_popup() as page_info:
            self.page.locator("div").filter(has_text=re.compile(r"^帮助手册$")).nth(1).click()
        helpdoc = page_info.value
        return helpdoc

    def contact_us(self):
        self.page.locator("div").filter(has_text=re.compile(r"^联系我们$")).nth(1).click()

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
        self.click_by_text('简体中文')
        self.click_by_text('English')
        self.page.wait_for_load_state()
        self.click_by_text('English')
        self.click_by_text('日本語')
        self.page.wait_for_load_state()
        self.click_by_text('日本語')
        self.click_by_text('简体中文')
