# -*- coding: utf-8 -*-
import time
import allure
import pytest
from allure_commons._allure import step
from page_objects.Migrationtool.field_page import MigrationField


@pytest.fixture(scope='class')
def migration_field(request, page, env):
    migration_field = MigrationField(page)
    request.cls.migration_field = migration_field
    migration_field.login_again()
    # 当前页面：第2页
    migration_field.click_by_button("开始解析")

    time.sleep(2)
    migration_field.click_by_button("下一步")
    time.sleep(2)
    migration_field.click_by_button("下一步")
    time.sleep(2)
    # migration_field.click_by_button("下一步")
    # migration_field.page.wait_for_timeout(2)
    # _, is_v = migration_field.is_viaible('//*[text()="请选择 Jira 项目"]', wait_time=3)
    # if is_v:
    #     migration_field.click_some_checkbox()
    # # 当前页面：第5页
    # if migration_field.is_viaible("请选择 Jira 项目"):
    #     migration_field.click_some_checkbox()
    # else:
    #     migration_field.click_by_button("下一步")
    # time.sleep(2)
    migration_field.click_by_button("下一步")
    time.sleep(2)
    migration_field.click_by_button("下一步")
    time.sleep(2)
    yield migration_field


@pytest.mark.usefixtures('migration_field', 'env')
@allure.story('Jira迁移工具-7.迁移属性')
class TestMigrationField:
    @allure.title('T206589 迁移属性-页面布局检查')
    @pytest.mark.run(order=1)
    def test_migration_field_layout(self, migration_field):
        with step("检查迁移操作说明"):
            migration_field.contains("迁移操作说明：")
            migration_field.contains("系统属性的映射规则已确定，不可更改。")

        with step("hover迁移操作说明"):
            # pass
            # migration_field.hover("")
            migration_field.page.get_by_role("cell", name="* 迁移操作").get_by_role("img").click()
            # migration_field.page.locator("//*[text()='迁移操作']/following-sibling::*").click()
            migration_field.contains("创建为 ONES 新的自定义属性")
            migration_field.contains("ONES 系统属性的映射规则已确定，不可更改")
            # migration_field.page.get_by_role("tooltip", name="1. 迁移操作说明： 1.1 创建：创建为 ONES 新的自定义工作项类型； 1.2 映射：映射为 ONES 已有的工作项类型，仅支持一对一映射； 1.3 取消迁移：对应的 Jira 问题及业务数据将不会迁移至 ONES。 2. 迁移至 ONES 后，ONES 映射关系将无法更改。").get_by_text("映射：映射为 ONES 已有的工作项类型，仅支持一对一映射；").click()

    @allure.title('T206580 迁移属性，搜索属性')
    @pytest.mark.run(order=2)
    def test_search_field(self):
        migration_field = self.migration_field
        with step("搜索输入：ID"):
            time.sleep(1)
            migration_field.search_jira_pro("搜索 Jira 属性名称", "ID")
            time.sleep(1)
            migration_field.page.get_by_role("cell", name="问题属性 (1)").get_by_role("img").click()
            migration_field.page.get_by_role("cell", name="问题属性 (1)").get_by_role("img").click()

            migration_field.contains("系统属性")
            migration_field.contains("创建")

            migration_field.clear_search_field()

        with step("搜索输入：12345"):
            migration_field.search_jira_pro("搜索 Jira 属性名称", "12345")
            migration_field.element_is_exist('//div[text()="暂无匹配结果"]')
            migration_field.clear_search_field()

    @allure.title('T206588 迁移属性，属性列表检查')
    @pytest.mark.run(order=3)
    def test_check_field_list(self):
        migration_field = self.migration_field
        with step("查看「迁移属性」列表-Jira 属性"):
            migration_field.contains("问题属性")
            migration_field.contains("项目")
        with step("查看「迁移属性」列表-Jira 属性类型宝包含：系统属性"):
            migration_field.contains("系统属性")
        with step("查看「迁移属性」列表-迁移效果"):
            migration_field.contains("不支持自助迁移")
        with step("查看「迁移属性」列表-迁移操作"):
            migration_field.contains("映射")
            migration_field.contains("创建")
            migration_field.contains("取消迁移")
        with step("查看「迁移属性」列表-ONES 工作项属性"):
            pass
            # migration_field.contains("工作项类型")
        with step("查看「迁移属性」列表-ONES属性类型"):
            migration_field.contains("系统属性")

    @allure.title('T207010 迁移属性，属性图例检查')
    @pytest.mark.run(order=4)
    def test_check_field_icon(self):
        migration_field = self.migration_field
        with step("hover至ONES 属性名称-描述旁边的问号"):
            migration_field.page.get_by_role("cell", name="描述").get_by_role("img").click()

        with step("hover至ONES 属性名称-关联发布旁边的问号"):
            migration_field.page.get_by_role("cell", name="关联发布").locator("path").nth(1).click()

    @allure.title('迁移属性，保存迁移属性配置')
    @pytest.mark.run(order=5)
    def test_check_field_conf(self):
        migration_field = self.migration_field
        with step("点击「上一步」"):
            migration_field.click_by_button("上一步")
            time.sleep(2)
        with step("在「选择 Jira项目」页面，点击「下一步」"):
            migration_field.click_by_button("下一步")
            time.sleep(2)
        with step("查看页面配置"):
            migration_field.contains("ID")
            migration_field.visible('//span[text()="取消迁移"]')

    @allure.title('T206583 迁移属性，映射列表可选值检查')
    @pytest.mark.run(order=6)
    def test_check_field_rule_value(self, page, migration_field):
        with step("Resolution 迁移操作设置为「映射」查看ONES工作项属性可选值"):
            # migration_field.check_field_rule_value(page)
            pass

    @allure.title('T207009 迁移属性，映射规则检查')
    @pytest.mark.run(order=7)
    def test_check_field_rule(self, page, migration_field):
        with step("Resolution 迁移操作设置为「映射」，查看ONES工作项属性可选值"):
            migration_field.search_jira_pro("搜索 Jira 属性名称", "Resolution")
            migration_field.clear_search_field()

        with step("搜索属性：0000-文本框（单行），并设置为映射,查看ONES工作项属性可选值"):
            migration_field.search_jira_pro("搜索 Jira 属性名称", "0000-文本框（单行")
            time.sleep(1)
            if page.is_visible('//div[text()="暂无匹配结果"]'):
                return
            else:
                page.get_by_role("cell", name="创建").get_by_text("创建").click()
                page.get_by_text("映射", exact=True).click()
                page.locator('(//div[@class="ones-select-selector"])[2]').click()
                migration_field.contains("暂无数据")
            migration_field.clear_search_field()

        with step("搜索属性：Project Description，并设置为映射,查看ONES工作项属性可选值"):
            migration_field.search_jira_pro("搜索 Jira 属性名称", "Project Description")
            # page.locator('//input[@placeholder="搜索 Jira 属性名称"]').click()
            # page.locator(".ones-input-clear-icon").click()
            # time.sleep(1)
            # page.get_by_placeholder("搜索 Jira 属性名称").click()
            # page.get_by_placeholder("搜索 Jira 属性名称").fill("Project Description")
            time.sleep(1)
            page.get_by_role("cell", name="创建").get_by_text("创建").click()
            page.get_by_text("映射", exact=True).click()
            page.locator('(//div[@class="ones-select-selector"])[2]').click()
            migration_field.contains("暂无数据")
            migration_field.clear_search_field()

        with step("搜索属性：Project URL，并设置为映射,查看ONES工作项属性可选值"):
            migration_field.search_jira_pro("搜索 Jira 属性名称", "Project URL")
            # page.locator('//input[@placeholder="搜索 Jira 属性名称"]').click()
            # page.locator(".ones-input-clear-icon").click()
            # time.sleep(1)
            # page.get_by_placeholder("搜索 Jira 属性名称").click()
            # page.get_by_placeholder("搜索 Jira 属性名称").fill("Project URL")
            time.sleep(1)
            page.get_by_role("cell", name="创建").get_by_text("创建").click()
            page.get_by_text("映射", exact=True).click()
            page.locator('(//div[@class="ones-select-selector"])[2]').click()
            migration_field.contains("暂无数据")
            migration_field.clear_search_field()

    @allure.title('T206584 迁移属性，存在未设置的工作项属性')
    @pytest.mark.run(order=8)
    def test_no_ones_field(self, page, migration_field):
        with step("搜索属性：Affects Version/s，并设置为映射,查看ONES工作项属性可选值为空"):
            migration_field.search_jira_pro("搜索 Jira 属性名称", "Affects Version/s")
            time.sleep(1)
            # self.set_action_and_check_result(page, migration_field, "映射")
            ##-----------需要调试——————————————————————————————————————————
            self.set_action_and_check_result(page, "创建", "映射")
            migration_field.clear_search_field()

        with step("搜索属性：Labels，并设置为映射,查看ONES工作项属性可选值为空"):
            migration_field.search_jira_pro("搜索 Jira 属性名称", "Labels")
            time.sleep(1)
            # self.set_action_and_check_result(page, migration_field, "映射")
            self.set_action_and_check_result(page, "创建", "映射")
            migration_field.clear_search_field()

        with step("搜索属性：Component/s，并设置为映射,查看ONES工作项属性可选值为空"):
            migration_field.search_jira_pro("搜索 Jira 属性名称", "Component/s")
            time.sleep(1)
            # self.set_action_and_check_result(page, migration_field, "映射")
            self.set_action_and_check_result(page, "创建", "映射")
            migration_field.clear_search_field()

    @allure.title("T206592 迁移属性，默认迁移操作检查")
    @pytest.mark.run(order=9)
    def test_default_action(self, page, migration_field):
        with step("查看「迁移属性」列表-默认「映射」的属性"):
            migration_field.search_jira_pro("搜索 Jira 属性名称", "Status")
            migration_field.contains("映射")
            migration_field.clear_search_field()

        with step("查看「迁移属性」列表-默认「创建」的属性"):
            migration_field.search_jira_pro("搜索 Jira 属性名称", "Resolution")
            migration_field.contains("创建")
            migration_field.clear_search_field()

        with step("查看「迁移属性」列表-默认「取消迁移」的属性"):
            migration_field.search_jira_pro("搜索 Jira 属性名称", "部署概览")
            migration_field.contains("取消迁移")
            migration_field.clear_search_field()

        with step("查看底部迁移属性统计"):
            migration_field.contains('个属性取消迁移')
            migration_field.contains("个属性不支持自助迁移")

    @allure.title("T206582 迁移属性，ONES工作项属性无可选值检查")
    @pytest.mark.run(order=10)
    def test_field_disable_click(self, page, migration_field):
        with step("点击展开单行文本 的迁移操作下拉框，选择「映射」"):
            migration_field.search_jira_pro("搜索 Jira 属性名称", "单行")
            time.sleep(1)
            _, is_v = migration_field.visible('//div[text()="暂无匹配结果"]')
            if is_v:
                pass
            else:
                migration_field.set_action_and_check_result(page, "创建", "映射")
            migration_field.clear_search_field()

    @allure.title("T206590 迁移属性，迁移操作选择：取消迁移")
    @pytest.mark.run(order=11)
    def test_set_cancel_operate(self, page, migration_field):
        with step("史诗名称  迁移操作设置为「取消迁移」"):
            migration_field.search_jira_pro("搜索 Jira 属性名称", "史诗名称")
            time.sleep(1)
            _, is_v = migration_field.visible('//div[text()="暂无匹配结果"]')
            if is_v:
                pass
            else:
                self.set_action_and_check_result(page, migration_field, "取消迁移")
            migration_field.clear_search_field()

    @allure.title("T206587 迁移属性，迁移操作选择：创建")
    @pytest.mark.run(order=12)
    def test_set_create_operate(self, page, migration_field):
        with step("史诗名称  迁移操作设置为「创建」"):
            migration_field.search_jira_pro("搜索 Jira 属性名称", "史诗名称")
            time.sleep(1)
            _, is_v = migration_field.visible('//div[text()="暂无匹配结果"]', wait_time=3)

            if is_v:
                pass
            else:
                migration_field.set_action_and_check_result(page, "创建", "创建")
                migration_field.visible('//span[text()="单行文本"]')
            migration_field.clear_search_field()

    @allure.title("T206586 迁移属性，迁移操作选择：映射")
    @pytest.mark.run(order=13)
    def test_set_map_operate(self, page, migration_field):
        with step("Resolution 迁移操作设置为「映射」，查看ONES工作项属性可选值"):
            # 先初始化一下
            migration_field.set_resolution_to_create(page)
            migration_field.search_jira_pro("搜索 Jira 属性名称", "Resolution")
            time.sleep(1)
            migration_field.set_action_and_check_result(page, "创建", "映射")
            page.get_by_text("映射", exact=True).click()
            page.locator('(//input[@type="search"])[2]').click()
            migration_field.contains("需求类型")
            migration_field.contains("操作系统")
            migration_field.contains("浏览器")
            migration_field.clear_search_field()

        with step("ONES工作项属性选择「问题单分析」"):
            page.locator('//div[text()="问题单分析"]').click()
            migration_field.visible('//span[text()="单选菜单"]')

        with step("点击设置图标"):
            page.locator('//span[text()="单选菜单"]//following-sibling::*/*').click()

        with step("查看jira选项名称"):
            migration_field.contains("Done")
            migration_field.contains("完成")
            migration_field.contains("重复提交")
            migration_field.contains("Unresolved")
            migration_field.contains("无法再次复现")

        with step("点击展开ONES属性下拉列表，查看可选值"):
            page.locator('(//span[@title="基本场景漏测"])[1]').click()
            migration_field.contains("特殊场景漏测")
            migration_field.contains("重复问题")
            migration_field.contains("新需求引入")
            page.locator('//div[text()="编辑选项"]').click()
            time.sleep(2)

        with step("Done映射为「不修复」"):
            page.locator('//span[@title="修改引入"]').click()
            # page.locator('(//div[text()="需求不明确"])[1]')
            # page.mouse.wheel(0, 80)
            # page.mouse.move(0, 80)
            # page.element.press("ArrowDown")
            # page.locator('(//div[text()="不修复" and @class="ones-select-item-option-content"])[2]').click()
            #
            # element = page.locator('(//div[text()="不修复" and @class="ones-select-item-option-content"])[2]')
            # element.press("ArrowDown")
            # # element. ScrollIntoViewIfNeededAsync().click()
            time.sleep(2)
            # element = page.locator("div .rc-virtual-list-holder:visible:has-text('需求不明确'):visible").nth(0)
            # element.hover()
            # for i in range(10):
            #     element.press("ArrowDown")

            page.locator("div .rc-virtual-list-holder:visible:has-text('需求不明确'):visible").click()
            migration_field.click_by_button('确定')

            # 完成映射为「不修复」
            # page.locator('//div[text()="编辑选项"]').click()
            # page.locator('(//span[@title="基本场景漏测"])[1]').click()
            # page.locator('//div[text()="不修复"]').click()
            #
            # # solve later映射为「转需求」
            # page.locator('//div[text()="编辑选项"]').click()
            # page.locator('//span[@title="易用性问题"]').click()
            # page.locator('(//div[text()="转需求"])[3]').click()
