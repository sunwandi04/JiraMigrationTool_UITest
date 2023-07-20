# -*- coding: utf-8 -*-
import time

from page_objects.Migrationtool.login_page import LoginPage


class BackupPage(LoginPage):

    def guide_backing_up_data(self):
        with self.page.expect_popup() as popup_info:
            self.click_by_link("了解如何备份 Jira Server 数据")
        popup = popup_info.value
        return popup

    def guide_jira_home(self):
        with self.page.expect_popup() as popup_info:
            self.click_by_link("查看默认 Jira 本地文件路径")
        popup = popup_info.value
        return popup

    def not_choose_backup(self):
        self.click_by_button("开始解析")

    def start_analyze(self, title, text):
        self.select_option(title, text)
        self.click_by_button("开始解析")

    def analyze_wrong_format(self):
        self.click_by_title("错误格式测试包.zip")
        self.click_by_button("开始解析")

    def clear_chosen_backup(self):
        if self.page.locator("span.ones-select-selection-placeholder").is_hidden():
            self.click_by_button("取消迁移")
            time.sleep(1)
            self.click_by_dialog_button("取消迁移")
            time.sleep(0.5)
            self.login_auto()
        else:
            print("未选择备份包")

    def analyze_time(self):
        analyze_time = self.page.locator("div.oac-flex.oac-items-center").first.inner_text()
        return analyze_time

    def analyze_backup_result(self):
        analyze_result = self.page.locator("div.ones-table-content").first.inner_text()
        analyze_result = analyze_result.replace("\t", " ")
        return analyze_result

    def analyze_team_result(self):
        analyze_result = self.page.locator("div.ones-table-content").nth(1).inner_text()
        analyze_result = analyze_result.replace("\t", " ")
        return analyze_result
