#!/usr/bin/env bash

set -x
# run py.test ($@ to derive parameters from commandline)
py.test -k "$TESTS_TO_RUN"  -n=3 --alluredir=ui_automation_tests/allure-results &
pid="$!"

# trap process id to stop script using Control+C
trap "echo '=== Stopping PID $pid ==='; kill -SIGTERM $pid" SIGINT SIGTERM

wait $pid
