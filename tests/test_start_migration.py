import os
import re
import allure
import pytest
from allure_commons._allure import step
from playwright.sync_api import expect
from page_objects.Migrationtool.front_page import FrontPage


@pytest.fixture(scope='class')
def start_page(request, page):
    start_page = FrontPage(page)
    request.cls.start_page = start_page
    yield start_page


@pytest.mark.usefixtures('start_page')
@allure.story('Jira迁移工具-首页')
class TestStartMigration:

    @allure.title('切换语言')
    @pytest.mark.run(order=1)
    def test_change_language(self):
        start_page = self.start_page
        with step('切换为英文、日文'):
            start_page.change_language()
        with step('检查是否切换成功'):
            lang = start_page.page.get_by_role('button', name='简体中文')
            expect(lang).to_be_visible()

    @allure.title('下载 Jira 数据迁移清单')
    @pytest.mark.run(order=2)
    def test_download_documents(self):
        start_page = self.start_page
        with step('点击右上角 ? 图标'):
            start_page.page.locator("header").get_by_role("img").nth(2).click()
        with step('点击下载 Jira 数据迁移清单'):
            mappingfile = start_page.download_file()
            mappingfile.save_as('Jira 数据迁移清单.xlsx')
        with step('检查数据迁移清单是否下载成功'):
            assert os.path.exists('Jira 数据迁移清单.xlsx') is True

    @allure.title('查看帮助手册')
    @pytest.mark.run(order=3)
    def test_helpdoc_page(self):
        start_page = self.start_page
        with step('点击右上角 ? 图标'):
            start_page.page.locator("header").get_by_role("img").nth(2).click()
        with step('点击帮助手册'):
            helpdoc = start_page.help_doc()
            helpdoc.wait_for_load_state()
        with step('检查帮助手册链接是否正确'):
            expect(helpdoc).to_have_url('https://guide.ones.pro/wiki/#/team/LBrdb4wE/space/6XDAYB1a/page/EyHo79My')
        with step('关闭使用指南页面'):
            helpdoc.close()

    @allure.title('点击联系我们')
    @pytest.mark.run(order=4)
    def test_contact_us(self):
        start_page = self.start_page
        with step('点击右上角 ? 图标'):
            start_page.page.locator("header").get_by_role("img").nth(2).click()
        with step('点击联系我们'):
            start_page.contact_us()
        with step('检查是否弹出联系我们弹窗'):
            dialog_title = start_page.page.get_by_role("dialog", name="联系我们").get_by_text("联系我们", exact=True)
            expect(dialog_title).to_be_visible()
        with step("关闭弹窗"):
            start_page.click_by_button("我知道了")

    @allure.title('查看使用指南')
    @pytest.mark.run(order=5)
    def test_guide_page(self):
        start_page = self.start_page
        with step('点击使用指南'):
            guide = start_page.guide_page()
            guide.wait_for_load_state()
        with step('检查使用指南链接是否正确'):
            expect(guide).to_have_url('https://guide.ones.pro/wiki/#/team/LBrdb4wE/space/6XDAYB1a/page/EyHo79My')
        with step('关闭使用指南页面'):
            guide.close()

    @allure.title('开始迁移')
    @pytest.mark.run(order=6)
    def test_start_migrate(self):
        start_page = self.start_page
        with step('点击开始迁移'):
            start_page.start_migration()
        with step('点击条款弹窗-确定按钮'):
            start_page.dont_agree_terms()
        with step('检查是否停留在首页'):
            expect(start_page.page).to_have_url(re.compile(r".*/page/home"))
        with step('条款弹窗-勾选同意条款'):
            start_page.agree_terms()
        with step('检查是否跳转到「登录 ONES」页面'):
            expect(start_page.page).to_have_url(re.compile(r".*/analyze/environment"))

    @allure.title('开始评估')
    @pytest.mark.run(order=7)
    def test_start_assess(self):
        start_page = self.start_page
        with step('回到迁移工具首页'):
            start_page.click_by_text('Jira 迁移工具')
        with step('点击开始评估'):
            start_page.start_assess()
        with step('检查是否跳转到「选择 Jira 备份包」页面'):
            expect(start_page.page).to_have_url(re.compile(r".*/analyze/pack"))
