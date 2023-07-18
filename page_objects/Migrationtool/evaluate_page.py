from JiraMigrationTool_UITest.page_objects.Migrationtool.front_page import FrontPage
import re

class EvaluatePage(FrontPage):

    def start_jiraaccessone(self):
        self.click_by_label("选择 Jira 备份包")
        self.click_by_title("0712集成测试.zip")
        self.click_by_button("开始评估")
        self.click_by_text("解析中")

    def start_jiraaccess(self):
        self.click_by_title("0712集成测试.zip")
        self.click_by_button("开始评估")
        self.click_by_text("解析完成")

    def cancel_assess(self):
        self.click_by_button("取消评估")
