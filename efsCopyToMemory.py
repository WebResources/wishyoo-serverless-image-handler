import json
import boto3
import concurrent.futures
import os
import base64
import shutil
import time
import io
import sys

def lambda_handler(event, context):

    bucket_in = "wishyoo-sih-source"

    request = get_request()

    for item in event['Records']:
        body = str(item['body'])
        bodyDict = json.loads(body)

        key = bodyDict['efsPathIn']
        bucket_out = bodyDict['bucketOut']
        width = bodyDict['imageWidth']
        height = bodyDict['imageHeight']

        key_out = key.split('.')[0] + ".webp"


        binaryOutput = copyFileTMPMemory(key)
        save_S3_from_memory( io.BytesIO(binaryOutput), bucket_in, key)

        with concurrent.futures.ThreadPoolExecutor() as executor:

            imageLambda = executor.submit(invoke_SIH_lambda, bucket_in, key, width, height, request)
            imageJSON = imageLambda.result()

            image_str = imageJSON['body']
            res = base64.b64decode(image_str)

            filename = "/tmp/" + key_out.rsplit('/',1)[1]

            save_file(filename, res)
            save_S3(filename, bucket_out, key_out)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def save_S3_from_memory(buf, bucketName, keyName):

    s3 = boto3.resource('s3')

    object = s3.Object(bucketName, keyName)
    response = object.put(Body=buf)
    
    return True


def copyFileTMPMemory(filepath):

    output = b''

    with open('/mnt/efs/' + filepath, "rb") as f:
        output = f.read()

    return output


def get_request():

    with open('/var/task/request.txt', encoding='utf-8') as f:
        json_data = json.loads(f.read())

    return json_data


def invoke_SIH_lambda(bucket, key, width, height, event):

    data = '{"bucket":"'+bucket+'","key":"'+key+'","edits":{"resize":{"width":'+width+',"height":'+height+',"fit":"contain","background":{"r": 255,"g": 255,"b": 255,"alpha": 0}}}}'
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

  with open(filename, "wb") as f:
    f.write(data)

  return


def save_S3(localFileName, bucketName, keyName):

    s3Client = boto3.client('s3')

    if not os.path.exists(localFileName):
        time.sleep(2)
        print(f"os.path {localFileName} does not exist")

    if(os.path.exists(localFileName)):
        response = s3Client.upload_file(localFileName, bucketName, keyName)
        if response != None:
            print(f"response {response}")
    else:
        print(f"file {localFileName} does not exist")

    return True
