# -*- coding: utf-8 -*-
import re
import pytest
from allure_commons._allure import step
from playwright.sync_api import expect
from page_objects.Migrationtool.evaluate_page import EvaluatePage


@pytest.fixture(scope='class')
def access_page(request, page):
    access_page = EvaluatePage(page)
    request.cls.access_page = access_page
    access_page.start_assess()
    yield access_page


@pytest.mark.usefixtures('access_page')
class TestStartAccess:

    def test_clik_access(self):
        access_page = self.access_page
        with step("没有选择zip，直接点击「开始评估」"):
            access_page.click_by_button("开始评估")
            expect(access_page.page.get_by_text("请选择 Jira 备份包")).to_be_visible()

    def test_clik_accessone(self):
        access_page = self.access_page
        with step("选择zip，解析中重新权限备份包"):
            access_page.start_jiraaccessone()
            access_page.click_by_button("重新选择备份包")
            expect(access_page.page).to_have_url(re.compile(r"./page/analyze/pack"))
            expect(access_page.page.get_by_text("0712集成测试.zip")).to_be_visible()

    def test_clik_accesstwo(self):
        access_page = self.access_page
        with step("选择zip，解析中取消"):
            access_page.click_by_button("开始评估")
            access_page.click_by_text("解析中")
            expect(access_page.page.get_by_text("Jira 备份包信息解析中")).to_be_visible()
            access_page.click_by_button("取消评估")
            expect(access_page.page).to_have_url(re.compile(r".*/page/home"))

    def test_clik_accessthree(self):
        access_page = self.access_page
        with step("选择zip，点击「开始评估」"):
            access_page.click_by_button("开始评估")
            access_page.start_jiraaccess()
            expect(access_page.page.get_by_text("Jira 备份包信息解析完成")).to_be_visible()
            access_page.click_by_button("check 选择 Jira 备份包")

    def test_cancel_assess(self):
        access_page = self.access_page
        with step("取消评估"):
            access_page.cancel_assess()
            expect(access_page.page).to_have_url(re.compile(r".*/page/home"))
