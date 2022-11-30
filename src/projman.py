import argparse

def generateEstimationFile(args):
    print(f"generating {args.o} from {args.planningPath}")
    # read content from planning file path
    # create repo from planning file content
    # generate estimation file content from repo
    # write estimation file content to estimation file path

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
