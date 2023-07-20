import re
import time

from page_objects.Migrationtool.front_page import FrontPage
from page_objects.ONES import ones_data_prepare


class LoginPage(FrontPage):

    def login_ones(self, url, username, pwd):
        self.type("例：http://ones.cn 或 https://ones.cn", url)
        self.input("ONES 邮箱", username)
        self.input("ONES 密码", pwd)
        self.click_by_button("下一步")

    def login_auto(self):
        self.click_by_button("开始迁移")
        self.check(locator='')
        self.click_by_button('确定')
        login_env = ones_data_prepare.read_config()
        self.type("例：http://ones.cn 或 https://ones.cn", login_env["ones_env_url"])
        self.input("ONES 邮箱", login_env["ones_env_user"])
        self.input("ONES 密码", login_env["ones_env_pwd"])
        self.click_by_button("下一步")

    def login_again(self):
        self.click_by_button("开始迁移")
        self.check(locator='')
        self.click_by_button('确定')
        login_env = ones_data_prepare.read_config()
        self.type("例：http://ones.cn 或 https://ones.cn", login_env["ones_env_url"])
        self.input("ONES 邮箱", login_env["ones_env_user"])
        self.input("ONES 密码", login_env["ones_env_pwd"])
        self.click_by_button("下一步")
        time.sleep(1)
        continue_modal = self.page.locator("div").filter(has_text=re.compile(r"^迁移配置记录$")).first
        if continue_modal.is_visible():
            self.click_by_button("继续配置")
        else:
            print("首次迁移")

    def login_with_no_input(self):
        self.click_by_button("下一步")

    def login_reconfigure(self):
        self.click_by_button("重新配置")

    def login_continue(self):
        self.click_by_button("继续配置")

    def logout(self):
        self.page.locator("header img").click()
        self.click_by_text("退出登录")
