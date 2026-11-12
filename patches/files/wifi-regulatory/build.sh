#!/bin/sh
set -eu
exec bash "$(dirname -- "$0")/../build.sh" "$@"
