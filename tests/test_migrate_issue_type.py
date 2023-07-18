import re
import pytest
import allure
from allure_commons._allure import step
from playwright.sync_api import expect
from page_objects.Migrationtool.issue_type_page import IssueTypePage



@pytest.fixture(scope='class')
def issue_type_page(request,page,env):
    issue_type_page = IssueTypePage(page)
    request.cls.issue_type_page = issue_type_page
    issue_type_page.login_again()
    issue_type_page.goto_issue_type_page()
    yield issue_type_page


@pytest.mark.usefixtures('issue_type_page', 'env')
class TestMigrateIssueType:
    @allure.title('检查迁移问题类型页面名称')
    @pytest.mark.run(order=1)
    def test_page_name(self):
        issue_type_page = self.issue_type_page
        with step('检查页面名称'):
            page_name = issue_type_page.page.get_by_text("迁移问题类型").nth(1)
            expect(page_name).to_be_visible()

    @allure.title('检查默认工作项类型')
    def test_action_create(self):
        issue_type_page = self.issue_type_page
        with step('检查是否存在类型：Epic'):
            epic_issue_type = issue_type_page.page.locator("span").filter(has_text=re.compile(r"^Epic$"))
            expect(epic_issue_type).to_be_visible()
        with step('检查是否存在类型：子任务'):
            sub_issue_type = issue_type_page.page.get_by_text("子任务", exact=True)
            expect(sub_issue_type).to_be_visible
        with step('检查是否存在类型：Bug'):
            bug_issue_type = issue_type_page.page.get_by_text("Bug")
            expect(bug_issue_type).to_be_visible()
        with step('检查是否存在类型：Story'):
            story_issue_type = issue_type_page.page.get_by_text("Story")
            expect(story_issue_type).to_be_visible()
        with step('检查是否存在类型：Task'):
            task_issue_type = issue_type_page.page.get_by_text("Task")
            expect(task_issue_type).to_be_visible()









