# Project Management Tools

## Installation in Docker Container

### Build the Container

```
docker build -t pm-docker:latest .
```

### Create and start the container (first time)

* `cd` to the working directory of you planning project
* Then
```
docker run -it \
  --name planning \
  -e DISPLAY=$DISPLAY \
  -e WAYLAND_DISPLAY=$WAYLAND_DISPLAY \
  -e XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $XDG_RUNTIME_DIR/$WAYLAND_DISPLAY:$XDG_RUNTIME_DIR/$WAYLAND_DISPLAY \
  -v "$(pwd)":/workspace \
  pm-docker:latest bash
```

### Reuse the container

```
docker start -ai planning
```


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