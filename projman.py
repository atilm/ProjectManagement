import argparse

from src.services.domain.representation_reading.md_representation_reader import *
from src.services.domain.representation_reading.md_planning_file_to_model_converter import *
from src.services.domain.representation_reading.md_estimation_file_to_model_converter import *
from src.services.domain.representation_writing.md_representation_writer import *
from src.services.domain.representation_writing.md_model_to_estimation_file_converter import *
from src.services.domain.representation_writing.md_model_to_planning_file_converter import *
from src.domain.report_generator import *

def read_from_file(filePath: str) -> str:
    file = open(filePath, mode='r', encoding="utf-8")
    content = file.read()
    file.close()
    return content

def write_to_file(filePath: str, content: str) -> str:
    file = open(filePath, mode='w', encoding="utf-8")
    file.write(content)
    file.close()

def initPlanningFile(args):
    print(f"initialize planning file: {args.planningPath}")
    repo = TaskRepository()
    writer = MarkdownRepresentationWriter(ModelToMarkdownPlanningDocumentConverter())
    planningFileContent = writer.write(repo)
    write_to_file(args.planningPath, planningFileContent)

def generateEstimationFile(args):
    print(f"generating {args.o} from {args.planningPath}")
    
    reader = MarkdownRepresentationReader(MarkdownPlanningDocumentToModelConverter())
    writer = MarkdownRepresentationWriter(ModelToMarkdownEstimationDocumentConverter())

    planningFileContent = read_from_file(args.planningPath)
    repo = reader.read(planningFileContent)
    estimationFileContent = writer.write(repo)
    write_to_file(args.o, estimationFileContent)

def applyEstimationFile(args):
    print(f"applying {args.estimationPath} to {args.planningPath}")
    planningReader = MarkdownRepresentationReader(MarkdownPlanningDocumentToModelConverter())
    estimationReader = MarkdownRepresentationReader(MarkdownEstimationFileToModelConverter())
    planningWriter = MarkdownRepresentationWriter(ModelToMarkdownPlanningDocumentConverter())

    planningInput = read_from_file(args.planningPath)
    planningRepo = planningReader.read(planningInput)

    estimationInput = read_from_file(args.estimationPath)
    estimationRepo = estimationReader.read(estimationInput)

    planningRepo.updateEstimates(list(estimationRepo.tasks.values()))
    planningOutput = planningWriter.write(planningRepo)
    write_to_file(args.planningPath, planningOutput)

def generateReport(args):
    print(f"Report on {args.planningPath}:\n")

    planningReader = MarkdownRepresentationReader(MarkdownPlanningDocumentToModelConverter())
    planningInput = read_from_file(args.planningPath)
    planningRepo = planningReader.read(planningInput)

    reportGenerator = ReportGenerator()
    report = reportGenerator.generate(planningRepo)

    print(f"Velocity: {report.velocity} story points / day")
    print(f"Remaining work days: {report.remaining_work_days}")
    
    if (report.warnings):
        print("\nWarnings:\n")
    
    for warning in report.warnings:
        print(warning)

    print("\n")


argumentParser = argparse.ArgumentParser(prog="projman", description="Cli project management tools")

subparsers = argumentParser.add_subparsers(help="The action to perform")

initParser = subparsers.add_parser("init", help="Generate a planning file with the initial structure.")
initParser.add_argument("planningPath", help="Path to the planning file.")
initParser.set_defaults(func=initPlanningFile)

createEstimationFileParser = subparsers.add_parser("estimation", help="Generate an estimation file from the planning file.")
createEstimationFileParser.add_argument("planningPath", help="Path to the planning file.")
createEstimationFileParser.add_argument("-o", help="Specify the output path for the estimation file.")
createEstimationFileParser.set_defaults(func=generateEstimationFile)

applyEstimationParser = subparsers.add_parser("applyestimation", help="Update the planning file from the estimation file.")
applyEstimationParser.add_argument("planningPath", help="Path to the planning file.")
applyEstimationParser.add_argument("estimationPath", help="Path to the estimation file.")
applyEstimationParser.set_defaults(func=applyEstimationFile)

reportParser = subparsers.add_parser("report", help="Ouput a report about the specified palnning file.")
reportParser.add_argument("planningPath", help="Path to the planning file.")
reportParser.set_defaults(func=generateReport)

args = argumentParser.parse_args()
args.func(args)
