import re
import time

from page_objects.base_page import BasePage
from page_objects.Migrationtool.choose_jira_pro_page import ChooseJiraPro

class MigrationField(ChooseJiraPro):

    def clear_search_field(cls):
        # 清空搜索
        cls.page.locator('//input[@placeholder="搜索 Jira 属性名称"]').clear()

    def expand_fold_field(self):
        """

        :return:
        """
        # 问题属性展开/折叠
        self.page.locator('//span[text()="问题属性"]/preceding-sibling::*/*')

    def set_action_and_check_result(self, page, name, operate):
        # """
        #  目的：用于设置迁移操作，且校验内容
        # :param page: 当前页面
        # :param name: 当前已经显示的操作。可选值有创建、映射、取消迁移
        # :param operate: 需要进行的操作：创建、映射、取消迁移
        # :return:
        # """

        # page.locator(f'//span[@title="{name}"]').click()
        # time.sleep(0.5)
        # page.locator(f'//div[text()="{operate}"]').click()

        # page.get_by_title(f"{operate}").get_by_text(f"{operate}").click()
        # page.get_by_text(f"{operate}", exact=True).click()
        # 点击下拉框操作，并且传入operate值

        page.get_by_role("cell", name=f"{name}").get_by_title(f"{name}").click()
        page.locator(f'div .rc-virtual-list-holder-inner:visible:has-text("{operate}"):visible')

    def check_field_rule_value(self,page):
        """Resolution 迁移操作设置为「映射」查看ONES工作项属性可选值"""
        self.search_jira_pro("搜索 Jira 属性名称", "Resolution")
        time.sleep(0.5)
        # self.set_action_and_check_result(page, "创建", "映射")
        page.locator('//span[@title="创建"]').click()
        time.sleep(0.5)
        page.locator('//div[text()="映射"]').click()
        page.locator('(//span[@class="ones-select-selection-search"]/*)[2]').click()
        time.sleep(0.5)
        self.visible('//div[@title="浏览器"]')
        self.contains("浏览器")
        self.contains("操作系统")

    def set_resolution_to_create(self,page):
        """将已经设置为映射的resolution属性，重新设置为创建。目的：当地于给这个属性初始化"""
        self.search_jira_pro("搜索 Jira 属性名称", "Resolution")
        _,is_v = self.visible('//span[@title="映射"]')
        if is_v:
            page.locator('//span[@title="映射"]').click()
            page.locator('//div[text()="创建"]').click()
            self.set_action_and_check_result(page,"映射","创建")
        else:
            pass
        self.clear_search_field()


