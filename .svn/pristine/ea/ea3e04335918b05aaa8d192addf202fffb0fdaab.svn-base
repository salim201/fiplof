import unittest
from ..DbMigration import DbMigration
from .ProviderStub import ProviderStub
from .RepositoryStub import RepositoryStub


class DbMigrationTest(unittest.TestCase):
    def createMigration(self, nonExecutedFiles=[], errorFiles=[]):
        provider = ProviderStub(nonExecutedFiles)
        repository = RepositoryStub()
        repository.setErrorousFiles(errorFiles)
        migration = DbMigration(provider, repository)
        return migration, repository

    def test_migrate_withFiles_executeAllFiles(self):
        files = ['file1', 'file2', 'file3']
        (migration, repository) = self.createMigration(files)

        migration.migrate()

        self.assertEqual(repository.getExecutedFiles(), files)
        self.assertEqual(repository.getLastExecutedFile(), 'file3')

    def test_migrate_withScrambledFiles_executeFilesInOrder(self):
        files = ['file5', 'file2', 'file3', 'file1']
        (migration, repository) = self.createMigration(files)

        migration.migrate()

        self.assertEqual(repository.getExecutedFiles(), ['file1', 'file2', 'file3', 'file5'])
        self.assertEqual(repository.getLastExecutedFile(), 'file5')

    def test_migrate_withErrorousFile_stopExecution(self):
        files = ['file1', 'file2', 'file3', 'file4', 'file5']
        (migration, repository) = self.createMigration(files, errorFiles=['file5', 'file3'])

        migration.migrate()

        self.assertEqual(repository.getExecutedFiles(), ['file1', 'file2'])
        self.assertEqual(repository.getLastExecutedFile(), 'file2')

    def test_migrate_dontSaveEmptyLastFile(self):
        files = ['file3']
        (migration, repository) = self.createMigration(files, errorFiles=['file3'])

        migration.migrate()

        self.assertEqual(repository.getExecutedFiles(), [])
        self.assertEqual(repository.getLastExecutedFile(), '')


if __name__ == '__main__':
    unittest.main()
