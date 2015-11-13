#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <region> <zip file> <role_arn>"
    exit
fi

REGION=$1
FILE=$2
ROLE_ARN=$3

aws lambda create-function \
--region $REGION \
--function-name LambdaWithTwilio \
--zip-file fileb://$FILE \
--role $ROLE_ARN \
--handler lambda_function.lambda_handler \
--runtime python2.7 \
--memory-size 128 \
--timeout 10
