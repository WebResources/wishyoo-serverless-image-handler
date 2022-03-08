import json
import boto3

def lambda_handler(event, context):

    bucket = "wishyoo-sih-source"
    prefix = "dev/"

    bucketNameList = getPaginatorList(bucket, prefix)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def getPaginatorList(bucket, prefix):

    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects_v2') #list_objects_v2

    operation_parameters = {'Bucket': bucket,
                            'Prefix': prefix}

    print(operation_parameters)

    page_iterator = paginator.paginate(**operation_parameters)

    pageCount = 0
    keyList = []
    for page in page_iterator:
        pageCount += 1

    print(f"pageCount = {pageCount}")

    return keyList
