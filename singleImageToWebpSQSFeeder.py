import json
import boto3

def lambda_handler(event, context):

    jsonString = '{\"efsPathIn\":\"attachments/109464/109464.jpeg\",\"imageWidth\":\"246\",\"imageHeight\":\"320\"\"BucketOut\":\"wishyoo-sih-output\", \"keyOut\":\"attachments/109464/109464.jpeg\"}'

    sqsURL = "https://sqs.us-west-2.amazonaws.com/727869158831/single-image-to-webp-sqs"

    sendMessageSQS(sqsURL, jsonString)

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda SingleImageToWebSQSFeeder!')
    }

def sendMessageSQS(sqsURL, jsonString):

    sqs = boto3.client('sqs')

    response = sqs.send_message(
        QueueUrl=sqsURL,
        DelaySeconds=10,
        MessageAttributes={
            'jsonString': {
                'DataType': 'String',
                'StringValue': jsonString
            }
        },
        MessageBody=(
            str(jsonString)
        )
    )
