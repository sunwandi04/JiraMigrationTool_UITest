from page_objects.Migrationtool.evaluate_page import EvaluatePage

class ResultsPage(EvaluatePage):

    def finish_access(self):
        self.click_by_button("完成评估")

    def migrate_now(self):
        self.click_by_button("开始迁移")
        self.check(locator='')
        self.click_by_button('确定')

    def download_file_access(self):
        with self.page.expect_download() as download_info:
            self.click_by_button("下载评估报告")
        download_info = download_info.value
        return download_info

