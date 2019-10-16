#!/bin/bash

# ZAP host and port as set while running the ZAP
ZAP_HOST="127.0.0.1"
ZAP_PORT="8090"

start_active_scan() {

    SCAN_URL="http://$1:$2/"
    SCAN_URL+="JSON/ascan/action/scan/?"
    SCAN_URL+="zapapiformat=JSON&"
    SCAN_URL+="formMethod=GET&"
    SCAN_URL+="url=https://$3&"
    SCAN_URL+="recurse=&"
    SCAN_URL+="inScopeOnly=&"
    SCAN_URL+="scanPolicyName=&"
    SCAN_URL+="method=&"
    SCAN_URL+="postData=&"
    SCAN_URL+="contextId="

    # Start Active ZAP Scan
    SCAN_ID_RES=$(curl -s $SCAN_URL)

    # Parse for scan ID
    SCAN_ID=$(echo $SCAN_ID_RES | jq -r '.scan')

    echo Scan ID: $SCAN_ID
}

# Start the Active ZAP scan
start_active_scan $ZAP_HOST $ZAP_PORT $ZAP_TARGET_URL

wait_for_scan_to_complete() {

    STATUS_URL="http://$1:$2/"
    STATUS_URL+="JSON/ascan/view/status/?"
    STATUS_URL+="zapapiformat=JSON&"
    STATUS_URL+="apikey=&"
    STATUS_URL+="formMethod=GET&"
    STATUS_URL+="scanId=$SCAN_ID"

    SCAN_STATUS=0
    until [[ $SCAN_STATUS -eq 100 ]]; do
        sleep 10

        # Get Scan status
        SCAN_STATUS_RES=$(curl -s $STATUS_URL)

        # Parse scan status
        SCAN_STATUS=$(echo $SCAN_STATUS_RES | jq -r '.status')

        # Display status
        echo Scan $SCAN_STATUS% complete

        done

    echo Scan Complete
}

# Get the status of scan
wait_for_scan_to_complete $ZAP_HOST $ZAP_PORT

get_alerts() {

    ALERTS_URL="http://$1:$2/"
    ALERTS_URL+="JSON/core/view/alerts/?"
    ALERTS_URL+="zapapiformat=JSON&"
    ALERTS_URL+="formMethod=GET&"
    ALERTS_URL+="baseurl=https://$3&"
    ALERTS_URL+="start=&"
    ALERTS_URL+="count=&"
    ALERTS_URL+="riskId="

    curl -s $ALERTS_URL > ui_automation_tests/zap/results/alerts.json
}

get_report() {
REPORT_URL="http://$1:$2/"
    REPORT_URL+="OTHER/core/other/htmlreport/?"
    REPORT_URL+="formMethod=GET"

    curl -s $REPORT_URL > ui_automation_tests/zap/results/report.html
}

# This retrieves the report in HTMl format
get_alerts $ZAP_HOST $ZAP_PORT $ZAP_TARGET_URL
get_report $ZAP_HOST $ZAP_PORT
