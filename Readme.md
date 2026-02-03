# Project Management Tools

## Installation in Docker Container

### Build the Container

```
docker build -t pm-docker:latest .
```

### Use the script to run a self-removing interactive container

```
./run_planning.sh
```

This will run the image `pm-docker:latest` and mount the current working directory.
When you exit the container, the container will be removed automatically.

## Editable Installation

In the root directory (containing the file setup.py) run:

```pip install -e .```

to install an *editable* version of the application. I.e. changes you make to the python files will have immediate effect on the installed version (after reload).

Then you can start the application from any directory using:

```python -m projman init <relative_file_path>```

## Testing

Run all tests

`python -m unittest`

Run a single test file:

`python -m unittest tests.markdown_parser_test`