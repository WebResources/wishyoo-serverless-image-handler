import json
import boto3
import concurrent.futures
import os
import base64

def lambda_handler(event, context):

    bucket_in = "wishyoo-sih-source"
    bucket_out = "wishyoo-sih-output"

    for item in event['Records']:
        key = str(item['body'])
        key_out = key.split('.')[0] + ".webp"

        request = get_request()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            imageLambda = executor.submit(invoke_SIH_lambda, bucket_in, key, request)
            imageJSON = imageLambda.result()

        image_str = imageJSON['body']
        res = base64.b64decode(image_str)

        filename = key_out.rsplit('/',1)[1]

        save_file(filename, res)
        save_S3(filename, bucket_out, key_out)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def get_request():

    with open('/var/task/request.txt', encoding='utf-8') as f:
        json_data = json.loads(f.read())

    return json_data


def invoke_SIH_lambda(bucket, key, event):

    data = '{"bucket":"'+bucket+'","key":"'+key+'","edits":{"resize":{"width":246,"height":320,"fit":"contain","background":{"r": 255,"g": 255,"b": 255,"alpha": 0}}}}'
    enc = base64.b64encode(data.encode())  # utf-8 by default

    event['path'] = '/' + str(enc)[2:-1]
    path_str = event['path']

    payload = json.dumps(event)

    session = boto3.session.Session()
    client = session.client("lambda")

    response = client.invoke(FunctionName="ServerlessImageHandler-BackEndImageHandlerLambdaFu-sUpr1N5OFx9w",
                            InvocationType = "RequestResponse",
                            Payload        = payload)

    resultDict = {}
    resultDict = json.loads(response['Payload'].read().decode())

    return resultDict


def save_file(filename, data):

  with open("/tmp/" + filename, "wb") as f:
    f.write(data)

  return


def save_S3(localFileName, bucketName, keyName):

    s3Client = boto3.client('s3')

    response = s3Client.upload_file('/tmp/'+ localFileName, bucketName, keyName)
    if response != None:
        print(response)

    return True
