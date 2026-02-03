#!/usr/bin/env bash
set -euo pipefail

# Runs an interactive, self-removing container from pm-docker:latest
# Mounts the current working directory to /workspace.
# Pass any arguments to override the default command (bash).

IMAGE=${IMAGE:-pm-docker:latest}

# Base env and volumes for X11
DOCKER_ENV=(
  -e DISPLAY="${DISPLAY:-}"
)
DOCKER_VOL=(
  -v /tmp/.X11-unix:/tmp/.X11-unix
  -v "$(pwd)":"/workspace"
)

# Add Wayland env/volume if available and socket exists
if [[ -n "${WAYLAND_DISPLAY:-}" && -n "${XDG_RUNTIME_DIR:-}" && -S "$XDG_RUNTIME_DIR/$WAYLAND_DISPLAY" ]]; then
  DOCKER_ENV+=( -e WAYLAND_DISPLAY="${WAYLAND_DISPLAY}" -e XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR}" )
  DOCKER_VOL+=( -v "$XDG_RUNTIME_DIR/$WAYLAND_DISPLAY:$XDG_RUNTIME_DIR/$WAYLAND_DISPLAY" )
fi

# Default command is bash; allow overrides via script args
if [[ $# -eq 0 ]]; then
  CONTAINER_CMD=(bash)
else
  CONTAINER_CMD=("$@")
fi

exec docker run --rm -it \
  "${DOCKER_ENV[@]}" \
  "${DOCKER_VOL[@]}" \
  "${IMAGE}" \
  "${CONTAINER_CMD[@]}"
