# -*- coding: utf-8 -*-
import re

import allure
import pytest
from allure_commons._allure import step
from playwright.sync_api import expect

from page_objects.Migrationtool.backup_page import BackupPage


@pytest.fixture(scope='class')
def analyze_page(request, page):
    analyze_page = BackupPage(page)
    request.cls.analyze_page = analyze_page
    analyze_page.login_again()
    analyze_page.clear_chosen_backup()
    yield analyze_page


@pytest.mark.usefixtures('analyze_page')
@allure.story('Jira迁移工具-解析 Jira 备份包')
class TestAnalyzeBackup:
    @allure.title('检查Jira 备份包解析中页面')
    @pytest.mark.run(order=1)
    def test_analyze_inprogress(self):
        analyze_page = self.analyze_page
        with step('选择的Jira 备份包,点击开始解析'):
            analyze_page.click_by_label("选择 Jira 备份包")
            analyze_page.start_analyze("0712集成测试.zip", "0712集成测试.zip")

        with step('检查状态是否为解析中、解析预估时间是否正确'):
            expect(analyze_page.page.get_by_text("解析中")).to_be_visible()
            assert analyze_page.analyze_time() == "解析进度\n预计 1 分钟，剩余 1 分钟"

        with step('解析过程中, 点击下一步, 检查是否有Toast提示'):
            analyze_page.click_by_button("下一步")
            expect(analyze_page.page.get_by_text("正在解析中")).to_be_visible()

        with step('解析过程中, 点击重新选择备份包, 检查是否返回到选择备份包页面'):
            analyze_page.click_by_button("重新选择备份包")
            expect(analyze_page.page).to_have_url(re.compile(r".*/analyze/pack"))

    @allure.title('检查Jira 备份包解析完成页面')
    @pytest.mark.run(order=2)
    def test_backup_analyze_result(self):
        analyze_page = self.analyze_page
        with step('查看Jira 备份包解析结果'):
            analyze_page.click_by_button("开始解析")
            backup_result = analyze_page.analyze_result()
            team_result = analyze_page.analyze_team_result()

        with step('检查解析状态成、Jira 备份包信息、ONES 团队信息解析是否正确'):
            expect(analyze_page.page.get_by_text("解析完成")).to_be_visible()
            expect(analyze_page.page.get_by_text("ONES 服务器磁盘容量支持迁移")).to_be_visible()
            assert backup_result == "Jira 版本 项目数量 工作项数量 成员数量 附件总大小 附件数量 Jira 服务器 ID\n7.10.0 514 11029 322 0 KB 31938 B9OQ-VO5E-E4ZS-89ES"
            assert team_result == "ONES 团队信息 迁移状态 迁移时间 Jira 服务器 ID\n\nP1000-wanditest\n 未迁移 - -\n\nzz_team1\n 未迁移 - -\n\nzz_team2\n 未迁移 - -"

    @allure.title('检查上一步、下一步页面跳转')
    @pytest.mark.run(order=3)
    def test_page_back_next(self):
        analyze_page = self.analyze_page
        with step('点击上一步，检查是否回到「选择 Jira 备份包」页面'):
            analyze_page.click_by_button("上一步")
            expect(analyze_page.page).to_have_url(re.compile(r".*/analyze/pack"))
            analyze_page.click_by_button("开始解析")

        with step('点击下一步，检查是否进入「选择 ONES 团队」页面'):
            analyze_page.click_by_button("下一步")
            expect(analyze_page.page).to_have_url(re.compile(r".*/analyze/team"))
            analyze_page.click_by_button("上一步")

    @allure.title('检查点击开始解析，进入解析结果页面')
    @pytest.mark.run(order=5)
    def test_cancel_analyze(self):
        analyze_page = self.analyze_page
        with step('选择备份包，点击开始解析'):
            analyze_page.click_by_text("错误格式测试包.zip")
            analyze_page.start_analyze("jira_ui_auto_test.zip", "jira_ui_auto_test.zip")
        with step('检查否跳转到「解析Jira 备份包」页面'):
            expect(analyze_page.page).to_have_url(re.compile(r".*/analyze/progress"))

    @allure.title('返回至选择 Jira 备份包页面，检查所选备份包是否保留')
    @pytest.mark.run(order=6)
    def test_save_backup_choose(self):
        analyze_page = self.analyze_page
        with step('点击「上一步」'):
            analyze_page.click_by_button("上一步")
        with step('检查所选备份包名称'):
            expect(analyze_page.page.get_by_text("jira_ui_auto_test.zip")).to_be_visible()

    @allure.title('返回至未完成的迁移配置，点击继续配置，检查是否进入「解析 Jira 备份包」页面')
    @pytest.mark.run(order=5)
    def test_reconfigure(self, env):
        analyze_page = self.analyze_page
        with step('退出登录'):
            analyze_page.logout()

        with step('再次登录，点击「重新配置」'):
            analyze_page.login_auto()
            analyze_page.login_continue()

        with step('检查是否进入「解析 Jira 备份包」页面'):
            expect(analyze_page.page).to_have_url(re.compile(r".*/analyze/progress"))
