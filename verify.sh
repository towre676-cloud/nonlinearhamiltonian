#!/bin/sh
set -eu
cd "$(dirname "$0")"
exec python3 -B -X utf8 -S verification/verify_publication.py "$@"
