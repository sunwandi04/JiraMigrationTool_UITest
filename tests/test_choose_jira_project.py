# -*- coding: utf-8 -*-
import time

import allure
import pytest
from allure_commons._allure import step
from playwright.sync_api import expect

# from page_objects.Migrationtool.backup_page import LoginPage
from page_objects.Migrationtool.choose_jira_pro_page import ChooseJiraPro


@pytest.fixture(scope='class')
def chooseproj_page(request, page, env):
    chooseproj_page = ChooseJiraPro(page)
    request.cls.chooseproj_page = chooseproj_page
    chooseproj_page.login_again()
    chooseproj_page.click_by_button("开始解析")
    time.sleep(3)
    chooseproj_page.click_by_button("下一步")
    time.sleep(3)
    chooseproj_page.click_by_button("下一步")
    yield chooseproj_page


@pytest.mark.usefixtures('chooseproj_page', 'env')
@allure.story('Jira迁移工具-5.选择jira项目')
class TestChooseJiraProject:
    @allure.title('T206170 选择jira项目-选择 Jira 项目，搜索项目')
    @pytest.mark.run(order=1)
    def test_search_jira_pro(self, chooseproj_page):
        now_time = time.strftime("%Y-%m-%d %H:%M:%S")
        with allure.step('搜索项目名称包含：示例项目'):
            chooseproj_page.search_jira_pro("搜索项目名称、Key、负责人", "示例项目")
            chooseproj_page.contains('示例项目')
            chooseproj_page.attach(png=f"搜索结果截图照片,{now_time}")
            chooseproj_page.clear_search_proj()

        with allure.step('搜索项目名称包含：TEST'):
            chooseproj_page.search_jira_pro("搜索项目名称、Key、负责人", "TEST")
            chooseproj_page.contains('test')
            chooseproj_page.attach(png=f"搜索结果截图照片,{now_time}")
            chooseproj_page.clear_search_proj()

        with allure.step('搜索项目名称包含：TEST123456789'):
            chooseproj_page.search_jira_pro("搜索项目名称、Key、负责人", "TEST123456789")
            chooseproj_page.element_is_exist('//div[text()="暂无匹配结果"]')
            chooseproj_page.attach(png=f"搜索结果截图照片,{now_time}")
            chooseproj_page.clear_search_proj()

    @allure.title('T206159 选择 Jira 项目，页面布局检查')
    @pytest.mark.run(order=2)
    def test_layout_data(self, chooseproj_page):
        # chooseproj_page = self.chooseproj_page
        with step("检查页面布局"):
            chooseproj_page = self.chooseproj_page
            chooseproj_page.contains("选择 Jira 项目")
            chooseproj_page.contains(
                "1. Jira 迁移工具仅支持迁移 Jira software 项目，即项目类型为“software”“business”的 Jira 项目。")
            chooseproj_page.contains(
                "2. 不支持自助迁移的项目及其业务数据将不予迁移，如果你需要迁移此类数据，请咨询 ONES 迁移团队。")

        # 检查"联系我们"弹框
        with step("选择jira项目页面，点击'联系我们'"):
            chooseproj_page = self.chooseproj_page
            chooseproj_page.page.locator("a").click()
            chooseproj_page.contains("感谢你的信任与支持")

        with step('检查是否弹出联系我们弹窗'):
            dialog_title = chooseproj_page.page.get_by_role("dialog", name="联系我们").get_by_text("联系我们", exact=True)
            expect(dialog_title).to_be_visible()
        with step("关闭弹窗"):
            chooseproj_page.click_by_button("我知道了")

    @allure.title('T206194 选择 Jira 项目，不支持自助迁移的项目')
    @pytest.mark.run(order=3)
    def test_not_support_pro_list(self, chooseproj_page):
        with step("打开不支持自助迁移的项目的弹框"):
            chooseproj_page = self.chooseproj_page
            chooseproj_page.not_support_pro()
            chooseproj_page.contains('不支持自助迁移的项目')

        with step("查看不支持自助迁移的项目总数量"):
            count_num = chooseproj_page.page.get_by_text("共 2 个")
            expect(count_num).to_be_visible()

        with step("查看不支持的项目列表表头"):
            chooseproj_page.contains("项目名称")
            chooseproj_page.contains("Key")
            chooseproj_page.contains("负责人")
            chooseproj_page.contains("项目分类")

        with step("搜索框输入：servicedesk"):
            chooseproj_page.page.get_by_role("dialog", name="不支持自助迁移的项目").get_by_placeholder(
                "搜索项目名称、Key、负责人").fill("servicedesk")
            chooseproj_page.contains('IT服务台-servicedesk')
            chooseproj_page.contains('IT')
            chooseproj_page.contains('肥仔果')
            chooseproj_page.contains('无分类')

        with step("点击「关闭」按钮"):
            chooseproj_page.click_by_button("关闭")

    @allure.title('T206157 选择 Jira 项目，选择所有项目')
    @pytest.mark.run(order=4)
    def test_choose_all_pro(self, chooseproj_page):
        with step("选择所有的项目"):
            chooseproj_page = self.chooseproj_page
            chooseproj_page.click_all_checkbox()
            count_num = chooseproj_page.page.get_by_text("已选0个")
            expect(count_num).not_to_be_visible()
            chooseproj_page.click_all_checkbox()

    @allure.title('T206156 选择 Jira 项目，选择部分项目')
    @pytest.mark.run(order=5)
    def test_choose_some_pro(self, chooseproj_page):
        with step("选择部分项目"):
            chooseproj_page = self.chooseproj_page
            chooseproj_page.click_some_checkbox()
            count_num = chooseproj_page.page.get_by_text("已选 1 个")
            expect(count_num).to_be_visible()

    @allure.title('T206158 选择 Jira 项目，检查项目排序')
    @pytest.mark.run(order=6)
    def test_proj_list_desc(self, chooseproj_page):
        with step("检查项目里的工作项数量"):
            chooseproj_page = self.chooseproj_page
            chooseproj_page.contains("386")
            chooseproj_page.contains("178")

    @allure.title('T206195 选择 Jira 项目，按负责人筛选项目')
    @pytest.mark.run(order=7)
    def test_filter_by_person(self, chooseproj_page):
        with step("表头「负责人」下拉框,选择负责人为jira"):
            chooseproj_page.page.get_by_role("cell", name="负责人").locator("path").click()
            chooseproj_page.filter_by_person(2)
            chooseproj_page.click_by_button("确定")
            chooseproj_page.contains("jira")
            chooseproj_page.contains("100+工作项类型")

        with step("表头「负责人」下拉框,选择负责人为wandi01"):
            chooseproj_page.page.get_by_role("cell", name="负责人").locator("path").click()
            chooseproj_page.filter_by_person(2)
            chooseproj_page.filter_by_person(3)
            chooseproj_page.click_by_button("确定")
            chooseproj_page.contains("wandi01")
            chooseproj_page.contains("0000-导入测试")

        with step("清除所选内容"):
            chooseproj_page.page.get_by_role("cell", name="负责人").locator("path").click()
            chooseproj_page.click_by_button("清空所选内容")
            chooseproj_page.click_by_button("确定")

    @allure.title('T206196 选择 Jira 项目，按项目分类筛选项目')
    @pytest.mark.run(order=8)
    def test_filter_by_type(self, chooseproj_page):
        with step("包含、类别1"):
            chooseproj_page.page.get_by_role("cell", name="项目分类").locator("path").click()
            chooseproj_page.filter_by_type(2)
            chooseproj_page.click_by_button("确定")
            chooseproj_page.contains("导入测试项目101")
            chooseproj_page.contains("导入测试项目103")
            chooseproj_page.contains("导入测试项目105")
        with step("包含、无分类"):
            chooseproj_page.page.get_by_role("cell", name="项目分类").locator("path").click()
            chooseproj_page.click_by_button("清空所选内容")
            chooseproj_page.filter_by_type(1)
            chooseproj_page.click_by_button("确定")
            chooseproj_page.contains("100+工作项类型")

        with step("包含、类别2"):
            chooseproj_page.page.get_by_role("cell", name="项目分类").locator("path").click()
            chooseproj_page.click_by_button("清空所选内容")
            chooseproj_page.filter_by_type(4)
            chooseproj_page.click_by_button("确定")
            chooseproj_page.contains("导入测试项目100")

        with step("包含、类别3"):
            chooseproj_page.page.get_by_role("cell", name="项目分类").locator("path").click()
            chooseproj_page.click_by_button("清空所选内容")
            chooseproj_page.filter_by_type(3)
            chooseproj_page.click_by_button("确定")
            chooseproj_page.contains("导入测试项目209")
