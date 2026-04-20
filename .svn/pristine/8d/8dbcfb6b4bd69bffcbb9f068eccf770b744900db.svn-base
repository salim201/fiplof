import unittest
from ..MigrationFilesProvider import MigrationFilesProvider
from .FilesystemStub import FilesystemStub
from .RepositoryStub import RepositoryStub


class MigrationFilesProviderTest(unittest.TestCase):
    def test_getNonExecutedFiles_withNonExistingFolder_returnsEmpty(self):
        fs = FilesystemStub({'/': [], 'migrations': ['file1.sql', 'file3.sql', 'file2.sql']})
        repository = RepositoryStub()
        provider = MigrationFilesProvider('foo', repository, fs)

        files = provider.getNonExecutedFiles()

        self.assertEqual(files, [])

    def test_getNonExecutedFiles_withoutPrevious_returnsAllFiles(self):
        fs = FilesystemStub({'/': [], 'migrations': ['file1.sql', 'file3.sql', 'file2.sql']})
        repository = RepositoryStub()
        provider = MigrationFilesProvider('migrations', repository, fs)

        files = provider.getNonExecutedFiles()

        self.assertEqual(files, ['migrations/file1.sql', 'migrations/file2.sql', 'migrations/file3.sql'])

    def test_getNonExecutedFiles_withPrevious_returnsRemainingFiles(self):
        fs = FilesystemStub({'/': [], 'migrations': ['file1.sql', 'file3.sql', 'file2.sql']})
        repository = RepositoryStub()
        repository.saveLastExecutedFile('migrations/file2.sql')
        provider = MigrationFilesProvider('migrations', repository, fs)

        files = provider.getNonExecutedFiles()

        self.assertEqual(files, ['migrations/file3.sql'])
