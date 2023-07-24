import re
import pytest
import allure
from allure_commons._allure import step
from playwright.sync_api import expect
from page_objects.Migrationtool.issue_type_page import IssueTypePage


@pytest.fixture(scope='class')
def issue_type_page(request, page, env):
    issue_type_page = IssueTypePage(page)
    request.cls.issue_type_page = issue_type_page
    issue_type_page.login_again()
    issue_type_page.goto_issue_type_page()
    yield issue_type_page


@pytest.mark.usefixtures('issue_type_page', 'env')
class TestMigrateIssueType:
    @allure.title('T206154 检查页面布局')
    @pytest.mark.run(order=1)
    def test_page_layout(self):
        issue_type_page = self.issue_type_page
        with step('检查页面标题'):
            page_title = issue_type_page.page.get_by_text("迁移问题类型").nth(1)
            expect(page_title).to_be_visible()
        with step('检查alter文案'):
            expect(issue_type_page.page.get_by_text("迁移操作说明：")).to_be_visible()
        with step('检查表头'):
            expect(issue_type_page.page.get_by_role("cell", name="Jira 问题类型", exact=True)).to_be_visible()
            expect(issue_type_page.page.get_by_role("cell", name="Jira 问题类型 ID")).to_be_visible()
            expect(issue_type_page.page.get_by_text("迁移操作", exact=True)).to_be_visible()
            expect(issue_type_page.page.get_by_text("*ONES 工作项类型")).to_be_visible()
        with step('检查存在的按钮'):
            expect(issue_type_page.page.get_by_role("button", name="取消迁移")).to_be_visible()
            expect(issue_type_page.page.get_by_role("button", name="上一步")).to_be_visible()
            expect(issue_type_page.page.get_by_role("button", name="下一步")).to_be_visible()
        with step('hover至「迁移操作」，检查tooltip文案'):
            issue_type_page.page.get_by_role("cell", name="* 迁移操作").get_by_role("img").hover()
            expect(issue_type_page.page.get_by_role("tooltip", name="1. 迁移操作说明： 1.1 创建：创建为 ONES 新的自定义工作项类型； 1.2 映射：映射为 ONES 已有的工作项类型，仅支持一对一映射； 1.3 取消迁移：对应的 Jira 问题及业务数据将不会迁移至 ONES。 2. 迁移至 ONES 后，ONES 映射关系将无法更改。")).to_be_visible()


    @allure.title('检查默认工作项类型')
    @pytest.mark.run(order=2)
    def test_issue_type(self):
        issue_type_page = self.issue_type_page
        with step('检查是否存在类型：Epic'):
            epic_issue_type = issue_type_page.page.locator("span").filter(has_text=re.compile(r"^Epic$"))
            expect(epic_issue_type).to_be_visible()
        with step('检查是否存在类型：子任务'):
            sub_issue_type = issue_type_page.page.get_by_text("子任务", exact=True).first
            expect(sub_issue_type).to_be_visible()
        with step('检查是否存在类型：Bug'):
            bug_issue_type = issue_type_page.page.get_by_text("Bug")
            expect(bug_issue_type).to_be_visible()
        with step('检查是否存在类型：Story'):
            story_issue_type = issue_type_page.page.get_by_text("Story")
            expect(story_issue_type).to_be_visible()
        with step('检查是否存在类型：Task'):
            task_issue_type = issue_type_page.page.get_by_text("Task")
            expect(task_issue_type).to_be_visible()

    # @allure.title('检查迁移操作：创建')
    # @pytest.mark.run(order=3)
    # def test_action_create(self):
    #     issue_type_page = self.issue_type_page
    #     with step('检查Epic的默认迁移操作'):
    #         issue_type_page.page.get_by_role("row", name="Epic 10000 创建 Epic").get_by_text("创建").click()
    #         issue_type_page.page.locator(".ones-select-item").first.click()
    #         expect(issue_type_page.page.get_by_role("row", name="Epic 10000 创建 创建 Epic").locator("div").filter(has_text="Epic").locator("span")).to_be_visible()

    # @allure.title('检查迁移操作：映射')
    # @pytest.mark.run(order=4)
    # def test_action_map(self):
    #     issue_type_page = self.issue_type_page
    #     issue_type_page.page.get_by_role("cell", name="映射 映射").get_by_title("映射").click()
    #     expect(issue_type_page.page.locator("[id=\"\\31 0000\"]")).to_be_visible()


    # @allure.title('检查迁移操作：取消迁移')
    # @pytest.mark.run(order=5)
    # def test_action_cancel(self):
    #     issue_type_page = self.issue_type_page
    #     issue_type_page.page.get_by_text("取消迁移").nth(3).click()
    #     expect(issue_type_page.page.get_by_text("-", exact=True)).to_be_visible()


    @allure.title('搜索')
    @pytest.mark.run(order=5)
    def test_search(self):
        issue_type_page = self.issue_type_page
        with step('搜索存在的工作项类型'):
            issue_type_page.search_input('搜索 Jira 问题类型名称、问题类型 ID', 'Bug')
            expect(issue_type_page.page.get_by_text("Bug")).to_be_visible()
        with step('搜索存在的工作项类型ID'):
            issue_type_page.search_input('搜索 Jira 问题类型名称、问题类型 ID', '10000')
            expect(issue_type_page.page.get_by_text("10000")).to_be_visible()
            expect(issue_type_page.page.locator("span").filter(has_text=re.compile(r"^Epic$"))).to_be_visible()
        with step('搜索不存在的内容'):
            issue_type_page.search_input('搜索 Jira 问题类型名称、问题类型 ID', '123456789023')
            expect(issue_type_page.page.get_by_text("暂无匹配结果")).to_be_visible()


    @allure.title('取消迁移')
    @pytest.mark.run(order=6)
    def test_cancel_migrate(self):
        issue_type_page = self.issue_type_page
        with step('点击取消迁移'):
            issue_type_page.click_by_button("取消迁移")
        with step('检查是否弹出二次确认弹窗'):
            expect(issue_type_page.page.get_by_text(
                "取消迁移后，相关迁移配置会被清除，并退出当前帐号回到工具首页。是否取消迁移？")).to_be_visible()
        with step('点击继续迁移'):
            issue_type_page.click_by_text("继续迁移")
        with step('检查是否弹窗关闭、停留在迁移问题类型页面'):
            expect(issue_type_page.page.get_by_text(
                "取消迁移后，相关迁移配置会被清除，并退出当前帐号回到工具首页。是否取消迁移？")).not_to_be_visible()
            expect(issue_type_page.page).to_have_url(re.compile(r".*/page/analyze/issue_map"))
        with step("取消迁移后检查是否会到首页"):
            issue_type_page.cancel_migrate()
            expect(issue_type_page.page).to_have_url(re.compile(r".*/page/home"))













