from .markdown_document import *

class MarkdownDocumentBuilder:
    def __init__(self) -> None:
        self.document = MarkdownDocument()

    def build(self):
        return self.document

    def withSection(self, text : str, level : int):
        self.document.append(MarkdownSection(text, level, lineNumber=-1))
        return self

    def withTable(self, table : MarkdownTable):
        self.document.append(table)
        return self

class MarkdownTableBuilder:
    def __init__(self) -> None:
        self.table = MarkdownTable(MarkdownTableRow([], -1))

    def build(self):
        return self.table

    def withHeader(self, *args):
        self.table._headerRow = MarkdownTableRow(args, -1)
        return self

    def withRow(self, *args):
        self.table.rows.append(MarkdownTableRow(args, -1))
        return self