import argparse
import os

from src.services.domain.representation_reading.md_representation_reader import *
from src.services.domain.representation_reading.md_multi_representation_reader import *
from src.services.domain.representation_reading.md_planning_file_to_model_converter import *
from src.services.domain.representation_reading.md_estimation_file_to_model_converter import *
from src.services.domain.representation_writing.md_representation_writer import *
from src.services.domain.representation_writing.md_model_to_estimation_file_converter import *
from src.services.domain.representation_writing.md_model_to_planning_file_converter import *
from src.domain.report_generator import *
from src.domain.task import VelocityCalculationException
from src.domain.completion_date_history import CompletionDateHistory
from src.services.utilities import string_utilities
from src.services.domain.report_generation.report_file_generator import ReportFileGenerator
from src.services.domain.graph_generation.burndown_graph_generator import BurndownGraphGenerator
from src.services.domain.graph_generation.graph_engine import GraphEngine
from src.services.domain.representation_reading.md_tracking_file_to_model_converter import MarkdownTrackingFileToModelConverter
from src.services.domain.representation_writing.md_model_to_tracking_file_converter import ModelToMarkdownTrackingFileConverter
from src.services.domain.graph_generation.project_tracking_graph_generator import ProjectTrackingGraphGenerator
from src.services.utilities.string_utilities import remove_suffix

# HELPERS ---------------------------------------------------------------------------------------

def catch_all(action, args):
    try:
        action(args)
    except TableRowException as e:
        print(e.message)
    except ConversionException as e:
        print(f"Could not  convert {e.inputString}.")
    except ValueConversionException as e:
        print(f"Could not convert {e.inputString} in line {e.lineNumber}.")
    except MarkdownConverterException as e:
        print(f"Markdown parsing error in line {e.lineNumber}.")
    except TaskIdConflictException as e:
        print(f"Found duplicate task id '{e.taskId}'")
    except VelocityCalculationException as e:
        print(f"Could not calculate velocity for story {e.task_id}.")
    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")

def read_from_file(filePath: str) -> str:
    file = open(filePath, mode='r', encoding="utf-8")
    content = file.read()
    file.close()
    return content

def write_to_file(filePath: str, content: str) -> str:
    file = open(filePath, mode='w', encoding="utf-8")
    file.write(content)
    file.close()

def parse_planning_files(planningPath: str) -> RepositoryCollection:
    planningReader = MarkdownMultiRepresentationReader(MarkdownPlanningDocumentToModelConverter())
    planningInput = read_from_file(planningPath)

    input_strings = [planningInput]

    absoluteFilePath = os.path.abspath(planningPath)
    directoryPath = os.path.dirname(absoluteFilePath)
    calendarPath = os.path.join(directoryPath, "Calendars")

    if os.path.exists(calendarPath):
        calendarFiles = os.listdir(calendarPath)
        for calendarFile in calendarFiles:
            input_strings.append(read_from_file(os.path.join(calendarPath, calendarFile)))

    return planningReader.read(input_strings)

def parse_tracking_file(projectId: str) -> CompletionDateHistory:
    tracking_file_path = to_tracking_file_path(projectId)
    
    file_content = read_from_file(tracking_file_path)
    tracking_reader = MarkdownRepresentationReader(MarkdownTrackingFileToModelConverter())
    history: CompletionDateHistory = tracking_reader.read(file_content)
    return history

def write_tracking_file(history: CompletionDateHistory) -> None:
    file_path = to_tracking_file_path(history.projectId)
    tracking_writer = MarkdownRepresentationWriter(ModelToMarkdownTrackingFileConverter())
    file_content = tracking_writer.write(history)
    write_to_file(file_path, file_content)
    
def to_tracking_file_path(projectId: str):
    # this function works with a project id
    # handle the case, where a file name is given instead
    projectId = remove_suffix(projectId, ".md")
    tracking_file_path = f"Tracking/{projectId}.md"
    return tracking_file_path

def parseDate(date_string: str) -> datetime.date:
    try:
        return string_utilities.parse_to_date(date_string)
    except:
        raise ValueConversionException(date_string, 0)

# Commands ------------------------------------------------------------------------------------

def initPlanningFile(args):
    print(f"initialize planning file: {args.planningPath}")
    task_repo = TaskRepository()
    working_days_repo = WorkingDayRepository()
    writer = MarkdownRepresentationWriter(ModelToMarkdownPlanningDocumentConverter())
    planningFileContent = writer.write(RepositoryCollection(task_repo, working_days_repo))
    write_to_file(args.planningPath, planningFileContent)

def generateEstimationFile(args):
    print(f"generating {args.estimationPath} from {args.planningPath}")
    
    reader = MarkdownRepresentationReader(MarkdownPlanningDocumentToModelConverter())
    writer = MarkdownRepresentationWriter(ModelToMarkdownEstimationDocumentConverter())

    planningFileContent = read_from_file(args.planningPath)
    repos = reader.read(planningFileContent)
    estimationFileContent = writer.write(repos)
    write_to_file(args.estimationPath, estimationFileContent)

def applyEstimationFile(args):
    print(f"applying {args.estimationPath} to {args.planningPath}")
    planningReader = MarkdownRepresentationReader(MarkdownPlanningDocumentToModelConverter())
    estimationReader = MarkdownRepresentationReader(MarkdownEstimationFileToModelConverter())
    planningWriter = MarkdownRepresentationWriter(ModelToMarkdownPlanningDocumentConverter())

    planningInput = read_from_file(args.planningPath)
    planningRepos = planningReader.read(planningInput)

    estimationInput = read_from_file(args.estimationPath)
    estimationRepo = estimationReader.read(estimationInput).task_repository

    planningRepos.task_repository.updateEstimates(list(estimationRepo.tasks.values()))
    planningOutput = planningWriter.write(planningRepos)
    write_to_file(args.planningPath, planningOutput)

def generateReport(args):
    print(f"Report on {args.planningPath}:\n")

    planningRepos = parse_planning_files(args.planningPath)

    reportGenerator = ReportGenerator()
    startDate = parseDate( args.startDate) if args.startDate else datetime.date.today()
    report = reportGenerator.generate(planningRepos, startDate)

    # for each project, append the currently predicted completion dates to a file to track the development of completion dates
    for projectId, completion_dates in report.predicted_completion_dates.items():
        history = parse_tracking_file(projectId)
        history.add(datetime.date.today(), completion_dates)
        write_tracking_file(history)

    # print summary to console
    print(f"Velocity: {report.velocity} story points / day")
    print("\nCompletion date ranges:")
    projectColumnWidth = max([len(projectId) for projectId in report.predicted_completion_dates.keys()])
    formatStr = f"{{0:>{projectColumnWidth}s}}: {{1}}"
    for projectId, completionDateInterval in report.predicted_completion_dates.items():
        print(formatStr.format(projectId, completionDateInterval.to_string(string_utilities.to_date_str)))

    if (report.warnings):
        print("\nWarnings:\n")
    
    for warning in report.warnings:
        print(warning)

    print("\n")

    if args.file:
        print(f"Write to report file: {args.file}")
        report_file_generator = ReportFileGenerator()
        report_file_content = report_file_generator.generate(report)
        write_to_file(args.file, report_file_content)

    if args.graph:
        print("Show a graph")
        graph_generator = BurndownGraphGenerator()
        graph_engine = GraphEngine()

        data = graph_generator.generate(report, planningRepos)
        graph_engine.plot_burndown_graph(data)

def formatFile(args):
    print(f"Reformat file {args.filePath}:\n")
    parser = MarkdownParser()
    writer = MarkdownWriter()

    input = read_from_file(args.filePath)
    document = parser.parse(input)
    output = writer.write(document)
    write_to_file(args.filePath, output)

def plotTrackingFile(args):
    history = parse_tracking_file(args.filePath)
    graph_generator = ProjectTrackingGraphGenerator()
    graph_engine = GraphEngine()
    data = graph_generator.generate(history)
    graph_engine.plot_tracking_graph(data)

argumentParser = argparse.ArgumentParser(prog="projman", description="Cli project management tools")

subparsers = argumentParser.add_subparsers(help="The action to perform")

initParser = subparsers.add_parser("init", help="Generate a planning file with the initial structure.")
initParser.add_argument("planningPath", help="Path to the planning file.")
initParser.set_defaults(func=lambda args: catch_all(initPlanningFile, args))

formatParser = subparsers.add_parser("format", help="Clean up the format of a markdown file (e.g. alignment in tables).")
formatParser.add_argument("filePath", help="The file to reformat.")
formatParser.set_defaults(func=lambda args: catch_all(formatFile, args))

createEstimationFileParser = subparsers.add_parser("estimate", help="Generate an estimation file from the planning file.")
createEstimationFileParser.add_argument("planningPath", help="Path to the planning file.")
createEstimationFileParser.add_argument("estimationPath", help="Specify the output path for the estimation file.")
createEstimationFileParser.set_defaults(func=lambda args: catch_all(generateEstimationFile, args))

applyEstimationParser = subparsers.add_parser("applyestimation", help="Update the planning file from the estimation file.")
applyEstimationParser.add_argument("planningPath", help="Path to the planning file.")
applyEstimationParser.add_argument("estimationPath", help="Path to the estimation file.")
applyEstimationParser.set_defaults(func=lambda args: catch_all(applyEstimationFile, args))

reportParser = subparsers.add_parser("report", help="Output a report about the specified planning file.")
reportParser.add_argument("planningPath", help="Path to the planning file.")
reportParser.add_argument("-f", "--file", help="Path to report file.")
reportParser.add_argument("-d", "--startDate", help="Date from when to start the predicition. If not specified, the current date is used.")
reportParser.add_argument("-g", "--graph", action='store_true', help="Show a burn down chart of all past and future stories")
reportParser.set_defaults(func=lambda args: catch_all(generateReport, args))

plotTrackingFileParser = subparsers.add_parser("track", help="Plot a graph of the historically predicted completion date ranges of the specified project.")
plotTrackingFileParser.add_argument("filePath", help="Path to the tracking file.")
plotTrackingFileParser.set_defaults(func=lambda args: catch_all(plotTrackingFile, args))

args = argumentParser.parse_args()
args.func(args)
