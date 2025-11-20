from .markdown_document import *
from projman.src.services.utilities import list_utilities

class MarkdownWriter:
    def write(self, document : MarkdownDocument) -> str:
        markdownString = ""

        for entry in document.getContent():
            if isinstance(entry, MarkdownSection):
                markdownString += self._sectionToString(entry)
            elif isinstance(entry, MarkdownTable):
                markdownString += self._tableToString(entry)

        return markdownString

    def _sectionToString(self, section : MarkdownSection):
        levelIndicator = (section.level + 1) * "#"
        return f"{levelIndicator} {section.title}\n\n"

    def _tableToString(self, table : MarkdownTable):
        columnWidths = table.getColumnWidths()

        tableString = ""
        tableString += self._writeTableRow(table._headerRow._cells, columnWidths)
        tableString += self._writeTableSeparator(columnWidths)
        for row in table.rows:
            tableString += self._writeTableRow(row._cells, columnWidths)
        tableString += "\n"

        return tableString

    def _writeTableSeparator(self, columnWidths : list) -> str:
        fields = [ width * '-' for width in columnWidths]
        return self._writeTableRow(fields, columnWidths)

    def _writeTableRow(self, entries : list, columnWidths : list) -> str:
        entries = list_utilities.fill_with(entries, len(columnWidths), "")

        rowString = "|"

        for idx, entry in enumerate(entries):
            rowString += f" {entry.ljust(columnWidths[idx])} |"

        return rowString + "\n"