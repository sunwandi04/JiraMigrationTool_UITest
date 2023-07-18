# -*- coding: utf-8 -*-
import re
import time
import allure
import pytest
from allure_commons._allure import step
from playwright.sync_api import expect
from JiraMigrationTool_UITest.page_objects.Migrationtool.login_page import LoginPage


@pytest.fixture(scope='class')
def login_page(request, page):
    login_page = LoginPage(page)
    request.cls.login_page = login_page
    login_page.start_migration()
    login_page.agree_terms()
    yield login_page


@pytest.mark.usefixtures('login_page', 'env')
@allure.story('Jira迁移工具-登录 ONES')
class TestLoginOnes:
    @allure.title('登录 ONES 输入校验')
    @pytest.mark.run(order=1)
    def test_login_no_input(self):
        login_page = self.login_page
        with step('点击下一步'):
            login_page.click_by_button("下一步")
        with step('检查是否提示请ONES 服务域名/IP'):
            expect(login_page.page.get_by_text("请输入 ONES 服务域名/IP")).to_be_visible()
        with step('检查是否提示ONES邮箱不能为空'):
            expect(login_page.page.get_by_text("请输入邮箱")).to_be_visible()
        with step('检查是否提示ONES密码不能为空'):
            expect(login_page.page.get_by_text("密码不能为空")).to_be_visible()

    @allure.title('登录 ONES，域名输入校验')
    @pytest.mark.run(order=2)
    def test_domain_input(self,env):
        login_page = self.login_page
        with step('输入错误格式域名'):
            login_page.login_ones("http://onescn", env["ones_env_common_user"], env["ones_env_pwd"])
            login_page.click_by_button("下一步")
            expect(login_page.page.get_by_text("请输入正确的 ONES 服务域名/IP")).to_be_visible()

        with step('输入错误格式 IP'):
            login_page.login_ones("http://11.22.33.", env["ones_env_common_user"], env["ones_env_pwd"])
            login_page.click_by_button("下一步")
            expect(login_page.page.get_by_text("请输入正确的 ONES 服务域名/IP")).to_be_visible()

        with step('输入无法访问地址'):
            login_page.login_ones("http://11.22.33.44", env["ones_env_common_user"], env["ones_env_pwd"])
            login_page.click_by_button("下一步")
            time.sleep(4.5)
            expect(login_page.page.get_by_text("请输入正确的 ONES 服务域名/IP")).to_be_visible()

    @allure.title('登录 ONES 密码错误 3 次')
    @pytest.mark.run(order=3)
    def test_wrong_pwd(self, env):
        login_page = self.login_page
        with step('输入正确ONES域名、正确ONES 邮箱、错误的ONES 密码'):
            login_page.login_ones(env["ones_env_url"], env["ones_env_user"], "Test12345")
        with step('检查否提示密码错误，还有 2 次尝试机会'):
            expect(login_page.page.get_by_text("帐号或密码错误，你还有 2 次尝试机会")).to_be_visible()
        with step('点击下一步'):
            time.sleep(1)
            login_page.click_by_button("下一步")
        with step('检查否提示密码错误，还有 1 次尝试机会'):
            expect(login_page.page.get_by_text("帐号或密码错误，你还有 1 次尝试机会")).to_be_visible()
        with step('点击下一步'):
            time.sleep(1)
            login_page.click_by_button("下一步")
        with step('检查否提示密码错误，还有 0 次尝试机会'):
            expect(login_page.page.get_by_text(
                "请到 ONES 环境下验证正确的帐号和密码，10 分钟后再重新登录此工具。")).to_be_visible()
        with step('点击确定'):
            login_page.click_by_button("确定")
        with step('检查是否回到首页'):
            expect(login_page.page).to_have_url(re.compile(r".*/page/home"))

    @allure.title('登录ONES, 账号无所有团队超级管理员权限')
    @pytest.mark.run(order=4)
    def test_login_not_allteam_admin(self, env):
        login_page = self.login_page
        with step('点击开始迁移'):
            login_page.start_migration()
            login_page.agree_terms()
        with step('输入正确的ONES域名、无权限账号、密码'):
            login_page.login_ones(env["ones_env_url"], env["ones_env_common_user"], env["ones_env_pwd"])
        with step('检查是否提示账号无权限'):
            expect(login_page.page.get_by_text(
                "此 ONES 账号非当前环境下所有 ONES 团队下超级管理员，请重新填写")).to_be_visible()

    @allure.title('登录ONES, 账号无组织管理员权限')
    @pytest.mark.run(order=5)
    def test_login_no_auth(self, env):
        login_page = self.login_page
        with step('输入正确的ONES域名、无权限账号、密码'):
            login_page.login_ones(env["ones_env_url"], env["ones_env_common_user2"], env["ones_env_pwd"])
        with step('检查是否提示账号无权限'):
            expect(login_page.page.get_by_text("此 ONES 账号非组织管理员，请重新填写")).to_be_visible()

    @allure.title('登录 ONES 成功,进入「选择 Jira 备份包」页面')
    @pytest.mark.run(order=6)
    def test_login_success(self, env):
        login_page = self.login_page
        with step('输入正确的ONES域名、账号、密码'):
            login_page.login_ones(env["ones_env_url"], env["ones_env_user"], env["ones_env_pwd"])
        with step('检查否跳转到「选择 Jira 备份包」页面'):
            expect(login_page.page).to_have_url(re.compile(r".*/analyze/pack"))

    @allure.title('返回至登录页面')
    @pytest.mark.run(order=7)
    def test_login_status(self):
        login_page = self.login_page
        with step('点击左上角工具名称'):
            login_page.click_by_button("上一步")
            login_page.click_by_text("Jira 迁移工具")
        with step('检查是否回到首页'):
            expect(login_page.page).to_have_url(re.compile(r".*/page/home"))
        with step('点击开始迁移'):
            login_page.start_migration()
        with step('检查是否显示已登录态'):
            expect(login_page.page.get_by_text("头像")).to_be_visible()

    @allure.title('取消迁移')
    @pytest.mark.run(order=8)
    def test_cancel_migrate(self):
        login_page = self.login_page
        with step('点击取消迁移'):
            login_page.click_by_button("取消迁移")
        with step('检查是否弹出二次确认弹窗'):
            expect(login_page.page.get_by_text(
                "取消迁移后，相关迁移配置会被清除，并退出当前帐号回到工具首页。是否取消迁移？")).to_be_visible()
        with step('点击继续迁移'):
            login_page.click_by_text("继续迁移")
        with step('检查是否弹窗关闭、停留在登录 ONES 页面'):
            expect(login_page.page.get_by_text(
                "取消迁移后，相关迁移配置会被清除，并退出当前帐号回到工具首页。是否取消迁移？")).not_to_be_visible()
            expect(login_page.page).to_have_url(re.compile(r".*/page/analyze/environment"))

    @allure.title('退出登录')
    @pytest.mark.run(order=9)
    def test_logout(self):
        login_page = self.login_page
        with step('点击右上角头像，退出登录'):
            login_page.logout()
        with step('检查是否回到首页'):
            expect(login_page.page).to_have_url(re.compile(r".*/page/home"))
