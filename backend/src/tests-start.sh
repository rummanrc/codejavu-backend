#! /usr/bin/env bash
set -e

python src/app/tests_pre_start.py

bash src/scripts/test.sh "$@"
