#!/bin/bash
set -eux

FUNCTION_NAME="aws-console-login-alert"
CODE_ZIP_FILE="code.zip"

cd ./src

zip -r $CODE_ZIP_FILE .

aws lambda update-function-code \
    --function-name $FUNCTION_NAME \
    --zip-file fileb://$CODE_ZIP_FILE \
    --no-cli-pager

rm -rf $CODE_ZIP_FILE