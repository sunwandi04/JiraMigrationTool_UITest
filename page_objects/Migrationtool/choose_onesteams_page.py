from page_objects.Migrationtool.backup_page import BackupPage

class SelectTeamPage(BackupPage):

    def select_team(self, name: str):
        self.type("搜索 ONES 团队名称", name)

    def select_row(self, cellname: str):
        self.expand_fold(cellname)
