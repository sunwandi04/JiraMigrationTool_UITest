from page_objects.migrationtool.front_page import FrontPage


class LoginPage(FrontPage):

    def login_ones(self, url, username, pwd):
        self.type("例：http://ones.cn 或 https://ones.cn", url)
        self.input("ONES 邮箱", username)
        self.input("ONES 密码", pwd)
        self.click_by_button("下一步")

    def login_with_no_input(self):
        self.click_by_button("下一步")

