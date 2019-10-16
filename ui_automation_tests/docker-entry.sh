#!/usr/bin/env bash

set -x

# Start zap proxy deamon
/usr/share/owasp-zap/zap.sh -daemon -config api.addrs.addr.regex=true -config api.disablekey=true -port 8090 -host 127.0.0.1 &
# Wait 10 seconds for zap daemon to start, sleep 10 will not work, the sleep will run in background.
for x in {1..10}; do sleep 1; done

# run py.test ($@ to derive parameters from commandline)
py.test -k "$TESTS_TO_RUN" --alluredir=ui_automation_tests/allure-results &
pid="$!"

# trap process id to stop script using Control+C
trap "echo '=== Stopping PID $pid ==='; kill -SIGTERM $pid" SIGINT SIGTERM

wait $pid

# generate zap proxy report
bash ui_automation_tests/zap/run.sh
