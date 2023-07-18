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
