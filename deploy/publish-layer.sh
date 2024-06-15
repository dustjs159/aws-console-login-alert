#!/bin/bash
set -eux

FUNCTION_NAME="aws-console-login-alert"
LAYER_NAME="$FUNCTION_NAME-layer"
LAYER_ZIP_FILE="layer.zip"

mkdir ./python && pip3 install -t ./python -r requirements.txt

zip -r $LAYER_ZIP_FILE python

aws lambda publish-layer-version \
    --layer-name $LAYER_NAME \
    --compatible-runtimes python3.12 \
    --zip-file fileb://$LAYER_ZIP_FILE \
    --no-cli-pager    

rm -rf $LAYER_ZIP_FILE ./python