import json
import boto3

def lambda_handler(event, context):

    bucket = "wishyoo-sih-source"
    prefix = "dev"

    sqsURL = "https://sqs.us-west-2.amazonaws.com/727869158831/process_image_file_to_webp"


    startPage = 0
    endPage = 2
    keysToReturnPerPage = 4

    keyNameList = getPaginatorList(bucket, prefix, startPage, endPage, keysToReturnPerPage)

    showKeyNameList(keyNameList)

    sendMessageSQS(bucket, sqsURL, keyNameList)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def showKeyNameList(keyNameList):

    print(f"keyCount = {len(keyNameList)}")

    if len(keyNameList) <= 10:
        for i in range(len(keyNameList)):
            print(f"{keyNameList[i]}")


def getPaginatorList(bucket, prefix, startPage, endPage, keysToReturnPerPage):

    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects')

    operation_parameters = {'Bucket': bucket,
                            'Prefix': prefix}

    page_iterator = paginator.paginate(**operation_parameters)

    pageCount = 0
    keyList = []
    for page in page_iterator:
        pageCount += 1

        lines = page['Contents']

        if pageCount >= startPage:
            lineCount = 0
            for line in lines:
                lineCount += 1
                key = line['Key']

                keyList.append(key)

                if lineCount >= keysToReturnPerPage:
                    break

        if pageCount >= endPage:
            break

    print(f"pageCount = {pageCount}")

    return keyList

def sendMessageSQS(bucket, sqsURL, listNames):

    sqs = boto3.client('sqs')

    for name in listNames:

        response = sqs.send_message(
            QueueUrl=sqsURL,
            DelaySeconds=10,
            MessageAttributes={
                'Bucket': {
                    'DataType': 'String',
                    'StringValue': bucket
                },
                'Key': {
                    'DataType': 'String',
                    'StringValue': str(name)
                }
            },
            MessageBody=(
                str(name)
            )
        )
