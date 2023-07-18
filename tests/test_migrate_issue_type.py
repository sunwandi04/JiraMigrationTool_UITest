import re
import pytest
from allure_commons._allure import step
from playwright.sync_api import expect
from page_objects.Migrationtool.issue_type_page import IssueTypePage



@pytest.fixture(scope='class')
def issue_type_page(request,page,env):
    issue_type_page = IssueTypePage(page)
    request.cls.issue_type_page = issue_type_page
    issue_type_page.login_again()
    yield issue_type_page


@pytest.mark.usefixtures('issue_type_page', 'env')
class TestMigrateIssueType:

    def test_page_name(self):
        issue_type_page = self.issue_type_page
        issue_type_page.goto_issue_type_page()
        with step('检查页面名称'):
            page_name = issue_type_page.page.get_by_text("迁移问题类型").nth(1)
            expect(page_name).to_be_visible()



