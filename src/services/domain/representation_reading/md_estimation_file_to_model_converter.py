from .md_converter_exceptions import *
from .representation_to_model_converter import *
from src.services.markdown.markdown_document import *

class MarkdownEstimationFileToModelConverter(IRepresentationToModelConverter):
    def convert(self, document: MarkdownDocument) -> TaskRepository:
        repo = TaskRepository()
        currentEstimate = None

        for item in document.getContent():
            if isinstance(item, MarkdownSection):
                currentEstimate = self._convert_to_estimate(item)
            if isinstance(item, MarkdownTable):
                for task in self._convert_table_to_tasks(item, currentEstimate):
                    repo.add(task)

        return repo

    def _convert_to_estimate(self, section: MarkdownSection) -> float:
        if self._is_title_section(section):
            return None
        elif self._is_unestimated_section(section):
            return None
        elif self._is_numbered_section(section):
            return float(section.title)
        else:
            raise UnexpectedSectionException(section.lineNumber)

    def _is_title_section(self, section: MarkdownSection):
        return section.level == 0 and section.title == "Estimation"

    def _is_unestimated_section(self, section: MarkdownSection):
        return section.title.strip() == "Unestimated"

    def _is_numbered_section(self, section: MarkdownSection):
        return self._is_float(section.title)

    def _is_float(self, input: any) -> bool:
        if input is None: 
            return False
        try:
            float(input)
            return True
        except ValueError:
            return False

    def _convert_table_to_tasks(self, table: MarkdownTable, estimate: float):
        if not(self._has_expected_header(table)):
            raise HeaderFormatException(table._headerRow.lineNumber)

        for r in table.rows:
            row: MarkdownTableRow = r
            if row.getColumnCount() != 2:
                raise ColumnNumberException(row.lineNumber)
            
            task = Task(row.get(0), row.get(1))
            task.estimate = estimate
            yield task

    def _has_expected_header(self, table: MarkdownTable) -> bool:
        return table._headerRow._cells == ["Id", "Desc"]