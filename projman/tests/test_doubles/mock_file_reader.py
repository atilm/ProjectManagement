from projman.src.services.file_reader import IFileReader

class MockFileReader(IFileReader):
    def __init__(self) -> None:
        self.content = ""

    def setup(self, fileContent : str):
        self.content = fileContent

    def readLines(self, filePath : str) -> list:
        return self.content.splitlines()

