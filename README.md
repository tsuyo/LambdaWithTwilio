# AWS Lambda with Twilio Demo

## Overview (How it works)

This python script is going to be deployed as AWS Lambda function. Event source type is Scheduled Event and periodically checks if a specified file on the web contains a word (which is also configured as parameter). If not, this function calls a specified phone number by Twilio API to alert.

## How to deploy this python script as AWS Lambda function
### create an artifact as zip
```bash
$ git clone https://github.com/tsuyo/LambdaWithTwilio.git
$ cd LambdaWithTwilio
$ cp config_template.py config.py
$ vi config.py # modify this to adjust your env
$ cat config.py
$ pip install -t=. twilio [*]
$ zip -r /tmp/LambdaWithTwilio.zip *
```
[\*] You might get an error at this command if you use python installed by Mac Homebrew. A workaround for this is as follows.
```bash
$ pyver=$(python --version 2>&1 | sed 's/Python //')
$ sudo vi $(find /usr/local -name distutils.cfg 2>/dev/null | grep $pyver)
...
[install]
force=1
#prefix=/usr/local # comment out this!
...
```
### create a test file (checked URL) and TwiML on S3 bucket
```bash
$ aws s3 mb s3://lambda-with-twilio
$ echo 'Hello World!' > hello.txt
$ echo '' > twilio.xml # An empty TwiML file is enough just to call
$ aws s3 cp hello.txt s3://lambda-with-twilio
$ aws s3 cp twilio.xml s3://lambda-with-twilio
$ aws s3api put-object-acl --bucket lambda-with-twilio --key hello.txt --acl public-read # make public
$ aws s3api put-object-acl --bucket lambda-with-twilio --key twilio.xml --acl public-read # make public
```
For much more useful TwiML (Twilio commands for a call), please refer to [TwiML: the Twilio Markup Language][1].

### create an IAM role

This is only done by AWS Management Console. Please refer to [Step 2.2: Create an IAM Role (execution role)][2].

### deploy zip file as Lambda function
You can create a lambda function by "aws lambda" command. Alternatively, a wrapper script in this repo can be used as follows. Check "role_arn" on AWS Management Console in advance.

```bash
$ ./aws_lambda_create_function.sh
Usage: ./aws_lambda_create_function.sh <region> <zip file> <role_arn>
$ ./aws_lambda_create.sh ap-northeast-1 ../LambdaWithTwilio.zip arn:aws:iam::<account_id>:role/executionrole
```
### create a scheduled event

Finally, you need a scheduled event which triggers this lambda function periodically. On MC, select "LambdaWithTwilio" function -> Event sources -> Add event source. Then, type "Scheduled Event" as Event source type.


[1]: https://www.twilio.com/docs/api/twiml
[2]: http://docs.aws.amazon.com/lambda/latest/dg/python-walkthrough-custom-events-create-test-function.html
[3]: http://docs.aws.amazon.com/lambda/latest/dg/getting-started-scheduled-events.html
