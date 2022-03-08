import json
import boto3
import os
import fnmatch

def lambda_handler(event, context):

    bucket = "wishyoo-sih-source"
    stage = "dev/"
    file_string = event['Records'][0]['body']
    file_list = list(file_string.split(","))

    count = 0
    for file in file_list:
        folderpath = '/mnt/efs/' + file

        count += 1
        if count < 10:
            print(f"{file}")

        get_filenames(folderpath, bucket, stage)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def get_filenames(folderpath, bucket, stage):

    for(path, dirs, files) in os.walk(folderpath, topdown=True):
        for filename in files:
            if fnmatch.fnmatch(filename, '*.jpeg') or fnmatch.fnmatch(filename, '*.jpg') or fnmatch.fnmatch(filename, '*.png'):
                filepath = os.path.join(path, filename)
                count += 1
                print(f"{filepath}")

                key = stage + filepath[9:]

 #               save_S3(filepath, bucket, key)


def save_S3(localFileName, bucketName, keyName):

    s3Client = boto3.client('s3')

    response = s3Client.upload_file(localFileName, bucketName, keyName)
    if response != None:
        print(response)

    return True
