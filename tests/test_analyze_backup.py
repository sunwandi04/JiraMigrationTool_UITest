# -*- coding: utf-8 -*-
import re
import allure
import pytest
from allure_commons._allure import step
from playwright.sync_api import expect
from JiraMigrationTool_UITest.page_objects.Migrationtool.backup_page import BackupPage


@pytest.fixture(scope='class')
def backup_page(request, page, env):
    backup_page = BackupPage(page)
    request.cls.backup_page = backup_page
    backup_page.login_again()
    yield backup_page


@pytest.mark.usefixtures('backup_page', 'env')
@allure.story('Jira迁移工具-登录 ONES')
class TestAnalyzeBackup:

    @allure.title('返回至未完成的迁移配置，点击继续配置，检查是否进入「解析 Jira 备份包」页面')
    @pytest.mark.run(order=1)
    def test_continue_configure(self, env):
        backup_page = self.backup_page
        with step('再次登录，点击「重新配置」'):
            backup_page.login_continue()
        with step('检查否跳转到「解析 Jira 备份包」页面'):
            expect(backup_page.page).to_have_url(re.compile(r".*/analyze/progress"))