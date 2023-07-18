from page_objects.Migrationtool.backup_page import BackupPage
import re

class IssueTypePage(BackupPage):
    def search_input(self, search_key):
        self.type("搜索 Jira 问题类型名称、问题类型 ID", search_key)

    def cancel_migrate(self):
        self.click_by_button("取消迁移")
        self.click_by_dialog_button("取消迁移")

    def choose_ones_org(self):
        self.page.get_by_label("", exact=True).check()
        self.click_by_button("下一步")

    def choose_jira_proj(self):
        self.page.get_by_role("row", name="0000-Jira 迁移测试 IMPORT 肥仔果 类别2 199").get_by_label("").check()
        self.click_by_button("下一步")

    def goto_issue_type_page(self):
        self.page.locator("div").filter(has_text=re.compile(r"^请选择$")).nth(4).click()
        self.start_analyze('0712集成测试.zip', '0712集成测试.zip')
        self.page.get_by_text("解析完成").click()
        self.click_by_button("下一步")
        self.choose_ones_org()
        self.choose_jira_proj()




