from page_objects.Migrationtool.backup_page import BackupPage
import re
import time


class IssueTypePage(BackupPage):
    def search_input(self, placeholder, search_key):
        self.type(placeholder, search_key)

    def cancel_migrate(self):
        self.click_by_button("取消迁移")
        self.click_by_dialog_button("取消迁移")

    def choose_ones_org(self):
        self.page.click(".ones-radio-input")
        self.click_by_button("下一步")

    def choose_jira_proj(self):
        # 选择导入项目：「0000-Jira迁移问题」
        self.page.locator('.ones-checkbox-input').nth(2).click()
        self.click_by_button("下一步")

    def first_goto_issue_type_page(self):
        self.page.locator("div").filter(has_text=re.compile(r"^请选择$")).nth(4).click()
        self.start_analyze('0712集成测试.zip', '0712集成测试.zip')
        self.click_by_text("解析完成")
        self.click_by_button("下一步")
        self.choose_ones_org()
        self.choose_jira_proj()

    # def Epic_type(self):
    #     tr_locator = self.page.locator('.ones-table-row ones-table-row-level-0').first()
    #     span_locator = tr_locator.locator('span')
    #     first_span_element = span_locator.first()
    #     expected_text = "Epic"
    #     actual_text = first_span_element.text_content()

    def goto_issue_type_page(self):
        if self.page.locator("span.ones-select-selection-placeholder").is_hidden():
            self.click_by_button("取消迁移")
            time.sleep(1)
            self.click_by_dialog_button("取消迁移")
            time.sleep(0.5)
            self.login_auto()
            self.first_goto_issue_type_page()
        else:
            self.first_goto_issue_type_page()

