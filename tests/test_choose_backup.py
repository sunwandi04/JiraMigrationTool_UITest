# -*- coding: utf-8 -*-
import re
import allure
import pytest
from allure_commons._allure import step
from playwright.sync_api import expect
from page_objects.Migrationtool.backup_page import BackupPage


@pytest.fixture(scope='class')
def backup_page(request, page, env):
    backup_page = BackupPage(page)
    request.cls.backup_page = backup_page
    backup_page.login_again()
    yield backup_page


@pytest.mark.usefixtures('backup_page', 'env')
@allure.story('Jira迁移工具-登录 ONES')
class TestChooseBackup:
    @allure.title('检查帮助文档跳转-备份 Jira Server 数据')
    @pytest.mark.run(order=1)
    def test_guide_backup_data(self):
        backup_page = self.backup_page
        with step('点击 了解如何备份 Jira Server 数据'):
            guide = backup_page.guide_backing_up_data()
        with step('检查帮助链接是否正确'):
            expect(guide).to_have_url('https://confluence.atlassian.com/adminjiraserver/backing-up-data-938847673.html')
        with step('关闭使用指南页面'):
            guide.close()

    @allure.title('检查帮助文档跳转-查看默认 Jira 本地文件路径')
    @pytest.mark.run(order=2)
    def test_guide_jira_home(self):
        backup_page = self.backup_page
        with step('点击 了解如何备份 Jira Server 数据'):
            guide = backup_page.guide_jira_home()
        with step('检查帮助链接是否正确'):
            expect(guide).to_have_url(
                'https://confluence.atlassian.com/adminjiraserver/jira-application-home-directory-938847746.html')
        with step('关闭使用指南页面'):
            guide.close()

    @allure.title('检查备份包必填')
    @pytest.mark.run(order=3)
    def test_not_choose_backup(self):
        backup_page = self.backup_page
        with step('不选择备份包，点击开始解析'):
            backup_page.not_choose_backup()
        with step('检查否提示请选择 Jira 备份包'):
            expect(backup_page.page.get_by_text("请选择 Jira 备份包")).to_be_visible()

    @allure.title('检查选择错误格式数据包，解析报错')
    @pytest.mark.run(order=4)
    def test_analyze_wrong_format(self):
        backup_page = self.backup_page
        with step('选择备份包，点击开始解析'):
            backup_page.click_by_label("选择 Jira 备份包")
            backup_page.analyze_wrong_format()
        with step('检查是否跳转到「解析Jira 备份包」页面,'):
            expect(backup_page.page).to_have_url(re.compile(r".*/analyze/progress"))
            expect(backup_page.page.get_by_text("解析失败，Jira 备份包数据格式错误，请重新上传")).to_be_visible()
        with step('点击「重新选择备份包」，检查是否回到「选择Jira 备份包」页面'):
            backup_page.click_by_button("重新选择备份包")
            expect(backup_page.page).to_have_url(re.compile(r".*/analyze/pack"))

    @allure.title('检查点击开始解析，进入解析结果页面')
    @pytest.mark.run(order=5)
    def test_start_analyze(self):
        backup_page = self.backup_page
        with step('选择备份包，点击开始解析'):
            backup_page.click_by_text("错误格式测试包.zip")
            backup_page.start_analyze()
        with step('检查否跳转到「解析Jira 备份包」页面'):
            expect(backup_page.page).to_have_url(re.compile(r".*/analyze/progress"))

    @allure.title('返回至选择 Jira 备份包页面，检查所选备份包是否保留')
    @pytest.mark.run(order=6)
    def test_save_backup_choose(self):
        backup_page = self.backup_page
        with step('点击「上一步」'):
            backup_page.click_by_button("上一步")
        with step('检查所选备份包名称'):
            expect(backup_page.page.get_by_text("jira_ui_auto_test.zip")).to_be_visible()

    @allure.title('返回至未完成的迁移配置，点击重新配置，检查是否进入「选择 Jira 备份包」页面')
    @pytest.mark.run(order=7)
    def test_reconfigure(self, env):
        backup_page = self.backup_page
        with step('退出登录'):
            backup_page.logout()
        with step('再次登录，点击「重新配置」'):
            backup_page.start_migration()
            backup_page.agree_terms()
            backup_page.login_ones(env["ones_env_url"], env["ones_env_user"], env["ones_env_pwd"])
            backup_page.login_reconfigure()
        with step('检查否跳转到「选择 Jira 备份包」页面'):
            expect(backup_page.page).to_have_url(re.compile(r".*/analyze/pack"))
            expect(backup_page.page.get_by_text("jira_ui_auto_test.zip")).to_be_visible()