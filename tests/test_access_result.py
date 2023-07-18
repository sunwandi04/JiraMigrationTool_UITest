import os
import re
import datetime

import pytest
from allure_commons._allure import step
from playwright.sync_api import expect
from JiraMigrationTool_UITest.page_objects.Migrationtool.assess_results import ResultsPage


@pytest.fixture(scope='class')
def result_page(request, page):
    result_page = ResultsPage(page)
    request.cls.result_page = result_page
    result_page.start_assess()
    result_page.click_by_label("选择 Jira 备份包")
    result_page.start_jiraaccess()
    yield result_page


@pytest.mark.usefixtures('result_page')
class TestAccessResult:

    def test_download_accessreport(self):
        result_page = self.result_page
        with step('下载评估报告'):
            mappingfile = result_page.download_file_access()
            now = datetime.datetime.now()
            formatted_date = now.strftime("%Y%m%d")
            print(mappingfile)
            mappingfile.save_as('0712集成测试.zip-迁移评估报告-'+formatted_date+'.xlsx')
        with step('检查下载评估报告是否下载成功'):
            assert os.path.exists('0712集成测试.zip-迁移评估报告-'+formatted_date+'.xlsx') is True

    def test_finish_access(self):
        result_page = self.result_page
        with step("完成评估"):
            result_page.finish_access()
            expect(result_page.page).to_have_url(re.compile(r".*/page/home"))

    def test_migrate_jiranow(self):
        result_page = self.result_page
        with step("开始迁移"):
            result_page.migrate_now()
            expect(result_page.page).to_have_url(re.compile(r".*/page/analyze/environment"))
