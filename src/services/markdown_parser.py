class MarkdownDocument:
    def __init__(self) -> None:
        self.content = []

    def getContent(self) -> list:
        return self.content

    def append(self, object) -> None:
        self.content.append(object)

class MarkdownSection:
    def __init__(self, title : str) -> None:
        self.title = title

class MarkdownTable:
    def __init__(self) -> None:
        pass


class MarkdownParser:
    def __init__(self) -> None:
        pass

    def parse(self, input : str) -> MarkdownDocument:
        document = MarkdownDocument()

        lines = input.splitlines()

        for line in lines:
            if self._isSection(line):
                document.append(self._createSection(line))

        return document

    def _isSection(self, line : str):
        return line.startswith('#')

    def _createSection(self, line : str):
        return MarkdownSection(line.strip().strip("#").strip())