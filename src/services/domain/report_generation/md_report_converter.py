from src.domain.report_generator import Report, TaskReport
from src.services.markdown.markdown_document import *
from src.services.markdown.markdown_document_builder import *
from src.services.utilities import string_utilities

class ReportToMarkdownConverter:
    def __init__(self) -> None:
        pass

    def convert(self, report: Report) -> MarkdownDocument:
        return MarkdownDocumentBuilder()\
            .withSection("Planning Report", 0)\
            .withTable(self._build_task_report_table(report.task_reports))\
            .build()

    def _build_task_report_table(self, taskReports: list) -> MarkdownTable:
        tableBuilder = MarkdownTableBuilder()\
            .withHeader("Id", "Description", "Days", "Completion date")

        for tr in taskReports:
            taskReport: TaskReport = tr
            tableBuilder.withRow(
                taskReport.taskId,
                taskReport.description,
                string_utilities.to_days_str(taskReport.estimated_days),
                string_utilities.to_date_str(taskReport.completion_date))

        return tableBuilder.build()