import argparse

from src.services.domain.representation_reading.md_representation_reader import *
from src.services.domain.representation_reading.md_planning_file_to_model_converter import *
from src.services.domain.representation_writing.md_representation_writer import MarkdownRepresentationWriter
from src.services.domain.representation_writing.md_model_to_estimation_file_converter import *
from src.services.domain.representation_writing.md_model_to_planning_file_converter import *

def read_from_file(filePath: str) -> str:
    file = open(filePath ,mode='r')
    content = file.read()
    file.close()
    return content

def write_to_file(filePath: str, content: str) -> str:
    file = open(filePath, mode='w')
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
    # read content from planning file path
    # create planningRepo from file content

    # read content from estimation file path
    # create estimationRepo from file content

    # udate estimates in planningRepo with content from estimationRepo
    # generate planning file content from planningRepo
    # write planning file content to planning file path


argumentParser = argparse.ArgumentParser(prog="projman",
    description="Cli project management tools")

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

args = argumentParser.parse_args()
args.func(args)
