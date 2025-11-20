import re
from typing import Iterable

from projman.src.services.domain.representation_reading.representation_to_model_converter import IRepresentationToModelConverter
from projman.src.domain.completion_date_history import *
from projman.src.services.markdown.markdown_document import *
from projman.src.services.domain.representation_reading.md_converter_exceptions import *
from projman.src.services.domain import markdown_configuration
from projman.src.services.utilities import string_utilities

unknownProjectString = "unknownProject"

class MarkdownTrackingFileToModelConverter(IRepresentationToModelConverter):
    def convert(self, document : MarkdownDocument) -> CompletionDateHistory:
        history = CompletionDateHistory(unknownProjectString)

        for item in document.getContent():
            if isinstance(item, MarkdownSection):
                history.projectId = self._convert_to_project_id(item)
            if isinstance(item, MarkdownTable):
                for record in self._convert_to_completion_date_records(item):
                    history.records.append(record)

        return history
    
    def _convert_to_project_id(self, section: MarkdownSection) -> str:
        m: re.Match[str] = re.match(r"(?P<projectId>.+)completion dates", section.title)

        if not(m):
            raise UnexpectedSectionException(section.lineNumber)

        return m.group('projectId').strip()
    
    def _convert_to_completion_date_records(self, table: MarkdownTable) -> Iterable[CompletionDateRecord]:
        if not(self._has_expected_header(table)):
            raise HeaderFormatException(table._headerRow.lineNumber)
        
        for r in table.rows:
            row: MarkdownTableRow = r
            if row.getColumnCount() != len(markdown_configuration.project_tracking_table_header):
                raise ColumnNumberException(row.lineNumber)
            
            try:
                record_date = string_utilities.parse_to_date(row.get(0))
                
                earliest_date = string_utilities.parse_to_date(row.get(1))
                probable_date = string_utilities.parse_to_date(row.get(2))
                latest_date = string_utilities.parse_to_date(row.get(3))
            except:
                raise ValueConversionException(row.lineNumber)
            
            completion_interval = ConfidenceInterval(earliest_date, probable_date, latest_date)
            

            comment = row.get(4)

            yield CompletionDateRecord(record_date, completion_interval, comment)


    def _has_expected_header(self, table: MarkdownTable) -> bool:
        return table._headerRow._cells == markdown_configuration.project_tracking_table_header