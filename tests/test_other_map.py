# -*- coding: utf-8 -*-
import time
import allure
import pytest
from playwright.sync_api import expect
from allure_commons._allure import step

from conftest import env
from page_objects.Migrationtool.other_map_page import OtherDataPage
from page_objects.Migrationtool.issue_type_page import IssueTypePage
from page_objects.Migrationtool.choose_jira_pro_page import ChooseJiraPro


@pytest.fixture(scope='class')
def other_map(request, page, env):
    other_map = OtherDataPage(page)
    request.cls.other_map = other_map
    other_map.login_again()
    # 当前页面：第2页
    other_map.click_by_button("开始解析")
    time.sleep(2)
    other_map.click_by_button("下一步")
    time.sleep(2)
    other_map.click_by_button("下一步")
    time.sleep(2)
    other_map.click_by_button("下一步")
    time.sleep(2)
    other_map.click_by_button("下一步")
    time.sleep(2)
    other_map.click_by_button("下一步")
    time.sleep(2)
    yield other_map

@pytest.mark.usefixtures('other_map', 'env')
@allure.story('Jira迁移工具-8.迁移其他数据')
class TestOtherData:
    @allure.title('T207017 Jira迁移工具-迁移其他数据，Jira 插件')
    @pytest.mark.run(order=1)
    def test_contains_jira_plugin(self, other_map):
        with step("点击展开Jira 插件"):
            other_map.expand_jira_module("Jira 用户安装插件")
            other_map.contains("Adaptavist ScriptRunner for JIRA")
            other_map.contains("不支持自助迁移")
            other_map.contains("插件")
            other_map.expand_jira_module("Jira 用户安装插件")

    @allure.title('T206597 Jira迁移工具-迁移其他数据，Jira 权限')
    @pytest.mark.run(order=2)
    def test_contains_jira_permission(self, other_map):
        with step("点击展开Jira 权限"):
            other_map.expand_jira_module("Jira 权限")
            other_map.contains("支持迁移")
            other_map.visible('//span[text()="可选权限成员域"]')
            other_map.visible('//span[text()="项目角色"]')
            other_map.expand_jira_module("Jira 权限")

    @allure.title('T207014 Jira迁移工具-迁移其他数据，Jira 通知')
    @pytest.mark.run(order=3)
    def test_contains_jira_permission(self, other_map):
        with step("点击展开Jira 通知"):
            other_map.expand_jira_module("Jira 通知")
            other_map.contains("通知对象")
            other_map.contains("当前经办人")
            other_map.contains("工作项负责人")
            other_map.contains("支持迁移")
            other_map.expand_jira_module("Jira 通知")

    @allure.title('T207012 Jira迁移工具-迁移其他数据，Jira 问题')
    @pytest.mark.run(order=4)
    def test_contains_jira_problem(self, other_map):
        with step("点击展开Jira 问题"):
            other_map.expand_jira_module("Jira 问题")
            other_map.contains("问题")
            other_map.contains("评论")
            other_map.contains("兼容迁移")
            other_map.expand_jira_module("Jira 问题")

    @allure.title('T207016 Jira迁移工具-迁移其他数据，Jira 系统配置')
    @pytest.mark.run(order=5)
    def test_contains_jira_config(self, other_map):
        with step("点击展开Jira 系统配置"):
            other_map.expand_jira_module("Jira 系统配置")
            other_map.contains("一般配置")
            other_map.contains("应用程序标题")
            other_map.contains("不支持自助迁移")
            other_map.expand_jira_module("Jira 系统配置")

    @allure.title('T207013 Jira迁移工具-迁移其他数据，Jira 项目')
    @pytest.mark.run(order=6)
    def test_contains_jira_proj(self, other_map):
        with step("点击展开Jira 项目"):
            other_map.expand_jira_module("Jira 项目")
            other_map.contains("项目角色")
            other_map.contains("名称")
            other_map.contains("名称")
            other_map.contains("支持迁移")
            other_map.expand_jira_module("Jira 项目")

    @allure.title('T207013 Jira迁移工具-迁移其他数据，Jira 用户')
    @pytest.mark.run(order=7)
    def test_contains_jira_user(self, other_map):
        with step("点击展开Jira 用户"):
            other_map.expand_jira_module("Jira 用户")
            other_map.contains("用户")
            other_map.contains("头像")
            other_map.contains("不支持自助迁移")
            other_map.contains("Jira 用户")
            other_map.expand_jira_module("Jira 用户")

    @allure.title("T206734 Jira迁移工具-迁移其他数据，页面布局检查")
    @pytest.mark.run(order=8)
    def test_check_layout(self,other_map):
        with step("查看「迁移其他数据」页面布局"):
            other_map.contains("其他数据映射，迁移操作既定，Jira 迁移工具将按照默认操作处理以下数据。")
            other_map.contains("如果你需要迁移「不支持自助迁移」的数据，或者需要自定义以下功能的迁移规则，请咨询 ONES 迁移团队。")

        with step("点击「联系我们」"):
            other_map.page.locator("a").click()
            other_map.contains("感谢你的信任与支持")
            dialog_title = other_map.page.get_by_role("dialog", name="联系我们").get_by_text("联系我们", exact=True)
            expect(dialog_title).to_be_visible()
            other_map.click_by_button("我知道了")

        with step("查看迁移数据列表"):
            other_map.contains("Jira 模块")
            other_map.contains("Jira 具体数据")
            other_map.contains("ONES 模块")
            other_map.contains("ONES 具体数据")
            other_map.contains("迁移效果")

        with step("查看迁移数据列表-分类"):
            other_map.contains("Jira 权限")
            other_map.contains("Jira 问题")
            other_map.contains("Jira 项目")
            other_map.contains("Jira 通知")
            other_map.contains("ira 用户")
            other_map.contains("Jira 系统配置")
            other_map.contains("Jira 用户安装插件")

    @allure.title("T207011 Jira迁移工具-迁移其他数据，搜索数据")
    @pytest.mark.run(order =8 )
    def test_search(self,other_map):
        with step("搜索框输入为空"):
            other_map.search_jira_pro("搜索 Jira 数据", "")
            other_map.contains("Jira 权限")
            other_map.clear_search_map()

        with step("搜索框输入：密码"):
            other_map.search_jira_pro("搜索 Jira 数据", "密码")
            other_map.contains("Jira 用户")
            other_map.expand_jira_module("Jira 用户")
            other_map.contains("密码")
            other_map.contains("不支持自助迁移")
            other_map.clear_search_map()

        with step("搜索框输入：问题已"):
            other_map.search_jira_pro("搜索 Jira 数据", "问题已")
            other_map.contains("Jira 通知")
            other_map.expand_jira_module("Jira 通知")
            other_map.contains("通知事件")
            other_map.contains("问题已更新")
            other_map.contains("创建工作项")
            other_map.contains("支持迁移")
            other_map.clear_search_map()

        with step("搜索框输入：TEST"):
            other_map.search_jira_pro("搜索 Jira 数据", "TEST")
            other_map.visible('//div[text()="暂无匹配结果"]')
            other_map.clear_search_map()