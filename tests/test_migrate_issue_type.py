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

    def test_title(self):
        issue_type_page = self.issue_type_page
        issue_type_page.goto_issue_type_page()
        with step('检查是否进入迁移问题类型页面'):
            expect(issue_type_page.page).to_have_url(re.compile(r".*/analyze/issue_map"))



