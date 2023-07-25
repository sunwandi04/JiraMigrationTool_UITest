# import re
# from page_objects.base_page import BasePage

#
# class FrontPage(BasePage):
#
#     def guide_page(self):
#         with self.page.expect_popup() as popup_info:
#             self.click_by_button("查看使用指南")
#         popup = popup_info.value
#         return popup
#
#     def download_file(self):
#         with self.page.expect_download() as download_info:
#             self.click_by_text("下载 Jira 数据迁移清单")
#         download_info = download_info.value
#         return download_info
#
#     def help_doc(self):
#         with self.page.expect_popup() as page_info:
#             self.page.locator("div").filter(has_text=re.compile(r"^帮助手册$")).nth(1).click()
#         helpdoc = page_info.value
#         return helpdoc
#
#     def contact_us(self):
#         self.page.locator("div").filter(has_text=re.compile(r"^联系我们$")).nth(1).click()
#
#     def start_migration(self):
#         self.click_by_button("开始迁移")
#
#     def start_assess(self):
#         self.click_by_button("开始评估")
#
#     def agree_terms(self, locator=''):
#         self.check(locator)
#         self.click_by_button('确定')
#
#     def dont_agree_terms(self, locator=''):
#         self.check(locator)
#         self.uncheck(locator)
#         self.click_by_button('确定')
#
#     def change_language(self):
#         self.click_by_text('简体中文')
#         self.click_by_text('English')
#         self.page.wait_for_load_state()
#         self.click_by_text('English')
#         self.click_by_text('日本語')
#         self.page.wait_for_load_state()
#         self.click_by_text('日本語')
#         self.click_by_text('简体中文')

import time

from page_objects.Migrationtool.backup_page import BackupPage


class ChooseJiraPro(BackupPage):

    def search_jira_pro(self, search_data, input_text):
        self.click_by_textbox(search_data, input_text)
        time.sleep(1)

    def guide_choose_jira_pro_data(self):
        self.page.locator("a").click()
        self.page.get_by_text("联系我们").click()

    def not_support_pro(self):
        # with self.page.expect_popup() as popup_info:
        #  self.page.click_by_button("不支持自助迁移的项目")
        # # popup = popup_info.value
        # return popup
        # print("popup的值为：-------------", popup)
        self.click_by_button("不支持自助迁移的项目")

    # 5.选择jira项目tab页，点击清除搜索按钮
    def clear_search_proj(self):
        # self.page.locator("div").filter(has_text=re.compile(r"^不支持自助迁移的项目$")).get_by_role("button").nth(1).click()
        self.search_jira_pro("搜索 Jira 属性名称", " ")

    def click_all_checkbox(self):
        self.page.locator(
            "//div[contains(@class,'ones-table-sticky-holder')]/descendant::input[@type='checkbox']").click()

    def click_some_checkbox(self):
        self.page.get_by_role("row", name="100+工作项类型 HUNDRED jira 无分类 386").get_by_label("").check()

    def filter_by_person(self, num):
        self.page.locator(
            f"div:nth-child({num}) > .ones-checkbox-wrapper > .ones-checkbox > .ones-checkbox-input").check()

    def filter_by_type(self, num):
        self.page.get_by_role("tooltip",
                              name="添加筛选条件 项目分类 包含 全选 无分类 类别1 类别3 类别2 清空所选内容 确定").get_by_label(
            "").nth(num).check()
