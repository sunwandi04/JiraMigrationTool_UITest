import time
from page_objects.Migrationtool.field_page import MigrationField

class OtherDataPage(MigrationField):
    # 展开jira模块，点击迁移的小三角
    def expand_jira_module(self, module_name):
        self.page.locator(f'//span[text()="{module_name}"]/preceding-sibling::span[1]/*').click()

    def clear_search_map(self):
        self.page.locator('//input[@placeholder="搜索 Jira 数据"]').clear()
