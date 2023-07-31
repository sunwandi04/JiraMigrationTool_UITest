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
    def clear_search_proj(cls ):
        # self.page.locator("div").filter(has_text=re.compile(r"^不支持自助迁移的项目$")).get_by_role("button").nth(1).click()
        cls.page.locator('//input[@placeholder="搜索项目名称、Key、负责人"]').clear()

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
