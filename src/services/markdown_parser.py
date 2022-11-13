from .file_reader import IFileReader

class Document:
    def __init__(self) -> None:
        self.content = []

    def getContent(self) -> list:
        return self.content

    def append(self, object) -> None:
        self.content.append(object)

class Section:
    def __init__(self) -> None:
        pass

class Table:
    def __init__(self) -> None:
        pass


class MarkdownParser:
    def __init__(self, file_reader : IFileReader) -> None:
        self.file_reader = file_reader

    def parse(self, filePath : str) -> Document:
        document = Document()

        lines = self.file_reader.readLines(filePath)

        if (len(lines) != 0):
            document.append(Section())

        return document