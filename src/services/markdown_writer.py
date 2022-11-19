from .markdown_document import *

class MarkdownWriter:
    def write(self, document : MarkdownDocument) -> str:
        markdownString = ""

        for entry in document.getContent():
            if entry is MarkdownSection:
                markdownString += self._sectionToString(entry)
            # elif entry is MarkdownTable:
            #     markdownString += self._tableToString(entry)

        return markdownString

    def _sectionToString(self, section : MarkdownSection):
        levelIndicator = (section.level + 1) * "#"
        return f"{levelIndicator} {section.title}\n\n"

    def _tableToString(self, table : MarkdownTable):
        array = self._toArray(table)
        columnWidths = self._findColumnWidths()

        tableString = ""
        tableString += self._writeTableRows(array[:1], columnWidths)
        tableString += self._writeTableSeparator(columnWidths)
        for row in table.rows:
            tableString += self._writeTableRow(row, columnWidths)
        tableString += "\n"

        return tableString

    def _toArray(self, table : MarkdownTable) -> list:
        result = []
        headers = table._headerRow._cells
        result.append(headers)

        for row in table.rows:
            result.append(self._normalize(row._cells, len(headers)))

        return result

    def _normalize(self, stringArray : list, fieldCount : int):
        if len(stringArray) >= fieldCount:
            return stringArray[:fieldCount]
        else:
            difference = (fieldCount - len(stringArray))
            return stringArray + [ "" for i in range(difference)]



