import re
from .markdown_document import *

class TableRowException(Exception):
    def __init__(self, lineNumber : int, *args: object) -> None:
        super().__init__(*args)
        self.message = f"No matching table header in line {lineNumber}"

class MarkdownParser:
    def __init__(self) -> None:
        self._tableRowRegex = re.compile(r"\|(.+\|)+")
        self._tableSeparatorRegex = re.compile(r"\|([\s-]+\|)+")
        self._state = self._parsingDocumentState

    def parse(self, input : str) -> MarkdownDocument:
        self._document = MarkdownDocument()
        self._currentTableItem = None

        lines = input.splitlines()

        previousLine = None

        for lineIdx, line in enumerate(lines):
            lineNumber = lineIdx + 1
            self._state(line, lineNumber, previousLine)
            previousLine = line

        if self._currentTableItem != None:
            self._document.append(self._currentTableItem)

        return self._document

    def _parsingDocumentState(self, line : str, lineNumber : int, previousLine : str):
        if self._isSection(line):
            self._document.append(self._createSection(line, lineNumber))
        elif self._isTableSeparator(line):
            self._currentTableItem = MarkdownTable(self._parseTableRow(previousLine, lineNumber - 1))
            self._state = self._parsingTableState

    def _parsingTableState(self, line : str, lineNumber : int, previousLine : str):
        if not line:
            self._document.append(self._currentTableItem)
            self._currentTableItem = None
            self._state = self._parsingDocumentState
        else:
            self._currentTableItem.rows.append(self._parseTableRow(line, lineNumber))

    def _isSection(self, line : str) -> bool:
        return line.startswith('#')

    def _isTableRow(self, line : str) -> bool:
        return self._tableRowRegex.match(line) != None

    def _parseTableRow(self, line : str, lineNumber : int) -> list:
        if not self._isTableRow(line):
            raise TableRowException(lineNumber)

        rawEntries = line.strip().strip("|").split("|")
        strippedEntries = [e.strip() for e in rawEntries]
        return MarkdownTableRow(strippedEntries, lineNumber)

    def _isTableSeparator(self, line : str) -> bool:
        return self._tableSeparatorRegex.match(line) != None

    def _createSection(self, line : str, lineNumber : int):
        dummyLevel = 0
        return MarkdownSection(line.strip().strip("#").strip(), dummyLevel, lineNumber)