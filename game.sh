#! /bin/bash

# If running from an extracted image, then export ARGV0 and APPDIR
if [ -z "${APPIMAGE}" ]; then
    export ARGV0=$0

    self="$(readlink -f -- $0)"
    here="${self%/*}"
    tmp="${here%/*}"
    export APPDIR="${tmp%/*}"
fi

cd "$APPDIR/opt/Game" && "$APPDIR/opt/python3.10/bin/python3.10" main.py
