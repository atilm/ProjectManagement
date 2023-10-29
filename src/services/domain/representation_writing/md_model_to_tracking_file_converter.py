from src.services.domain.representation_writing.model_to_representation_converter import IModelToRepresentationConverter
from src.domain.completion_date_history import *
from src.services.markdown.markdown_document import MarkdownDocument
from src.services.markdown.markdown_document_builder import *
from src.services.domain import markdown_configuration
from src.services.utilities import string_utilities

def toStr(date: datetime.date) -> str:
    return string_utilities.to_date_str(date)

class ModelToMarkdownTrackingFileConverter(IModelToRepresentationConverter):
    def convert(self, history : CompletionDateHistory) -> MarkdownDocument:
        builder = MarkdownDocumentBuilder()\
            .withSection(f"{history.projectId} completion dates", 0)\
            .withTable(self._records_to_table(history.records))
        
        return builder.build()
        
    def _records_to_table(self, records: list[CompletionDateRecord]):
        builder = MarkdownTableBuilder()\
            .withHeader(*markdown_configuration.project_tracking_table_header)

        for record in records:
            completion_date = record.completion_date_interval

            builder.withRow(toStr(record.date), 
                            toStr(completion_date.lower_limit),
                            toStr(completion_date.expected_value),
                            toStr(completion_date.upper_limit),
                            record.comment)

        return builder.build()
    
