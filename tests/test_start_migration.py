import re
import allure
import pytest
from allure_commons._allure import step
from playwright.sync_api import expect
from page_objects.front.front_page import FrontPage


@pytest.fixture(scope='class')
def start_page(request, page):
    start_page = FrontPage(page)
    request.cls.start_page = start_page
    yield start_page


@pytest.mark.usefixtures('start_page')
@allure.story('Jira迁移工具-首页')
class TestStartMigration:

    @allure.title('切换语言')
    def test_change_language(self):
        start_page = self.start_page
        with step('切换为英文、日文'):
            start_page.change_language()
        with step('检查是否切换成功'):
            lang = start_page.page.get_by_role('button', name='简体中文')
            expect(lang).to_be_visible()

    @allure.title('查看帮助文档')
    def test_guide_page(self):
        start_page = self.start_page
        with step('点击查看使用指南'):
            guide = start_page.guide_page()
            guide.wait_for_load_state()
        with step('检查使用指南链接是否正确'):
            expect(guide).to_have_url('https://guide.ones.pro/wiki/#/team/LBrdb4wE/space/6XDAYB1a/page/EyHo79My')
        with step('关闭使用指南页面'):
            guide.close()

    @allure.title('开始迁移')
    def test_start_migrate(self):
        start_page = self.start_page
        with step('点击开始迁移'):
            start_page.start_migration()
        with step('点击同意条款'):
            start_page.agree_terms()
        with step('检查是否跳转到「登录 ONES」页面'):
            expect(start_page.page).to_have_url(re.compile(r".*/analyze/environment"))

    @allure.title('开始评估')
    def test_start_assess(self):
        start_page = self.start_page
        with step('回到迁移工具首页'):
            start_page.click_by_text('Jira 迁移工具')
        with step('点击开始评估'):
            start_page.start_assess()
        with step('检查是否跳转到「选择 Jira 备份包」页面'):
            expect(start_page.page).to_have_url(re.compile(r".*/analyze/pack"))
