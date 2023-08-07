import re
import time

import pytest
from allure_commons._allure import step
from playwright.sync_api import expect
from page_objects.Migrationtool.choose_onesteams_page import SelectTeamPage


@pytest.fixture(scope='class')
def ones_team_page(request, page, env):
    ones_team_page = SelectTeamPage(page)
    request.cls.ones_team_page = ones_team_page
    ones_team_page.login_again()
    ones_team_page.click_by_button("开始解析")
    time.sleep(3)
    ones_team_page.click_by_button("下一步")
    yield ones_team_page


@pytest.mark.usefixtures('ones_team_page')
class TestChooseOnesTeam:
    def test_page_choose_teams(self):
        ones_team_page = self.ones_team_page
        with step('检查页面标题'):
            page_title = ones_team_page.page.get_by_text("选择 ONES 团队").nth(1)
            expect(page_title).to_be_visible()
        with step('检查表头'):
            expect(ones_team_page.page.get_by_role("cell", name="ONES 团队名称")).to_be_visible()
            expect(ones_team_page.page.get_by_role("cell", name="迁移状态")).to_be_visible()
            expect(ones_team_page.page.get_by_role("cell", name="Jira 备份包名称")).to_be_visible()
            expect(ones_team_page.page.get_by_role("cell", name="Jira 版本")).to_be_visible()
            expect(ones_team_page.page.get_by_role("cell", name="Jira 服务器 ID")).to_be_visible()
            expect(ones_team_page.page.get_by_role("cell", name="迁移时间")).to_be_visible()
        with step('检查存在的按钮'):
            expect(ones_team_page.page.get_by_role("button", name="取消迁移")).to_be_visible()
            expect(ones_team_page.page.get_by_role("button", name="上一步")).to_be_visible()
            expect(ones_team_page.page.get_by_role("button", name="下一步")).to_be_visible()

    def test_select_team(self):
        ones_team_page = self.ones_team_page
        with step('检查模糊搜索'):
            ones_team_page.select_team("team")
            expect(ones_team_page.page.get_by_text("zz_team1")).to_be_visible()
            expect(ones_team_page.page.get_by_text("zz_team2")).to_be_visible()
        with step('检查精准搜索'):
            ones_team_page.select_team("zz_team1")
            expect(ones_team_page.page.get_by_text("zz_team1")).to_be_visible()
            expect(ones_team_page.page.get_by_text("zz_team2")).not_to_be_visible()
        with step('检查无匹配结果搜索'):
            ones_team_page.select_team("不存在的团队")
            expect(ones_team_page.page.get_by_text("暂无匹配结果")).to_be_visible()
        with step('清空搜索内容'):
            ones_team_page.click(".ones-input-clear-icon")
            expect(ones_team_page.page.get_by_text("zz_team1")).to_be_visible()

    def test_choose_team(self):
        with step('使用团队名称筛选'):
            ones_team_page = self.ones_team_page
        with step('筛选包含'):
            ones_team_page.select_row("ONES 团队名称")
            ones_team_page.click(
                "//*[@class='ones-select oac-width-full oac-mb-2 ones-select-single ones-select-show-arrow']")
            ones_team_page.click("//*[@class='rc-virtual-list-holder']//*[text()='包含']")
            # ones_team_page.click("div .rc-virtual-list-holder-inner:visible:has-text('包含'):visible") 这种方式是模糊搜索，
            # 会把文本是'包含'的所有内容都找出来随机点
            ones_team_page.page.check("//*[text()='zz_team1']/preceding-sibling::label//input")
            ones_team_page.click_by_button("确定")
            expect(ones_team_page.page.get_by_role("cell", name="zz_team1")).to_be_visible()
            expect(ones_team_page.page.get_by_role("cell", name="zz_team2")).not_to_be_visible()
        with step('筛选不包含'):
            ones_team_page.select_row("ONES 团队名称")
            ones_team_page.click(
                "//*[@class='ones-select oac-width-full oac-mb-2 ones-select-single ones-select-show-arrow']")
            ones_team_page.click("//*[@class='rc-virtual-list-holder']//*[text()='不包含']")
            ones_team_page.page.check("//*[text()='zz_team1']/preceding-sibling::label//input")
            ones_team_page.click_by_button("确定")
            expect(ones_team_page.page.get_by_role("cell", name="zz_team1")).not_to_be_visible()
            expect(ones_team_page.page.get_by_role("cell", name="zz_team2")).to_be_visible()
        with step('筛选全选不包含'):
            ones_team_page.select_row("ONES 团队名称")
            ones_team_page.click(
                "//*[@class='ones-select oac-width-full oac-mb-2 ones-select-single ones-select-show-arrow']")
            ones_team_page.click("//*[@class='rc-virtual-list-holder']//*[text()='不包含']")
            ones_team_page.page.check("//*[text()='全选']/preceding-sibling::label//input")
            ones_team_page.click_by_button("确定")
            expect(ones_team_page.page.get_by_text("暂无数据")).to_be_visible()
        with step('清空所选内容'):
            ones_team_page.select_row("ONES 团队名称")
            ones_team_page.page.check("//*[text()='zz_team1']/preceding-sibling::label//input")
            ones_team_page.click_by_button("清空所选内容")
            ones_team_page.click_by_button("确定")
            expect(ones_team_page.page.get_by_role("cell", name="zz_team1")).to_be_visible()

    def test_choose_status(self):
        with step('使用迁移状态筛选'):
            ones_team_page = self.ones_team_page
            ones_team_page.page.reload()
        with step('筛选包含'):
            ones_team_page.select_row("迁移状态")
            expect(ones_team_page.page.get_by_text("清空所选内容")).to_be_visible()
            ones_team_page.click(
                "//*[@class='ones-select oac-width-full oac-mb-2 ones-select-single ones-select-show-arrow']")
            ones_team_page.click("//*[@class='rc-virtual-list-holder']//*[text()='包含']")
            # ones_team_page.click("div .rc-virtual-list-holder-inner:visible:has-text('包含'):visible") 这种方式是模糊搜索，
            # 会把文本是'包含'的所有内容都找出来随机点
            ones_team_page.page.check("//*[text()='未迁移']/preceding-sibling::label//input")
            ones_team_page.click_by_button("确定")
            expect(ones_team_page.page.get_by_role("cell", name="zz_team1")).to_be_visible()
            expect(ones_team_page.page.get_by_role("cell", name="zz_team2")).to_be_visible()
        with step('筛选不包含'):
            ones_team_page.select_row("迁移状态")
            ones_team_page.click(
                "//*[@class='ones-select oac-width-full oac-mb-2 ones-select-single ones-select-show-arrow']")
            ones_team_page.click("//*[@class='rc-virtual-list-holder']//*[text()='不包含']")
            ones_team_page.page.check("//*[text()='未迁移']/preceding-sibling::label//input")
            ones_team_page.click_by_button("确定")
            expect(ones_team_page.page.get_by_role("cell", name="zz_team1")).not_to_be_visible()
            expect(ones_team_page.page.get_by_role("cell", name="zz_team2")).not_to_be_visible()
        with step('筛选全选不包含'):
            ones_team_page.select_row("迁移状态")
            ones_team_page.click(
                "//*[@class='ones-select oac-width-full oac-mb-2 ones-select-single ones-select-show-arrow']")
            ones_team_page.click("//*[@class='rc-virtual-list-holder']//*[text()='不包含']")
            ones_team_page.page.check("//*[text()='全选']/preceding-sibling::label//input")
            ones_team_page.click_by_button("确定")
            expect(ones_team_page.page.get_by_text("暂无数据")).to_be_visible()
        with step('清空所选内容'):
            ones_team_page.select_row("迁移状态")
            ones_team_page.page.check("//*[text()='未迁移']/preceding-sibling::label//input")
            ones_team_page.click_by_button("清空所选内容")
            ones_team_page.click_by_button("确定")
            expect(ones_team_page.page.get_by_role("cell", name="zz_team1")).to_be_visible()

    def test_clik_next(self):
        ones_team_page = self.ones_team_page
        with step('不选择直接点击下一步'):
            ones_team_page.click_by_button("下一步")
            expect(ones_team_page.page.get_by_text("请选择 ONES 团队"))
        with step('选择团队，点击下一步'):
            # ones_team_page.page.get_by_role("row", name="zz_team1 未迁移 - - - -").get_by_label("").check()
            ones_team_page.page.check(
                "//*[text()='zz_team1']/parent::div/parent::*/preceding-sibling::*/descendant::label/span")
            expect(ones_team_page.page.get_by_text("已选「zz_team1」团队"))
            ones_team_page.click_by_button("下一步")
            expect(ones_team_page.page).to_have_url(re.compile(r".*/page/analyze/import_project"))

    def test_clik_teams(self):
        ones_team_page = self.ones_team_page
        with step('点击选择 ONES 团队的tab'):
            ones_team_page.click_by_button("check 选择 ONES 团队")
            expect(ones_team_page.page).to_have_url(re.compile(r".*/page/analyze/team"))
