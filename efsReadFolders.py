import json
import os
import fnmatch
import boto3

def lambda_handler(event, context):

    bucket = "wishyoo-sih-source"
    folder = ["attachments","signatures"]
    stage = 'dev/'

    for item in folder:
        folderpath = '/mnt/efs/' + item
        localFileName = '/tmp/'+item+'_folders.txt'

        os_list = os.listdir(folderpath)
        print(f"{stage} {item} {len(os_list)}")

        write_list(localFileName, os_list)
        save_S3(localFileName, bucket, 'image_path/'+ stage + item +'.txt')

#    if len(os_list) > 10:
#    print(os_list[0:10])

#    for item in os_list[:1000]:
#        get_filenames(folderpath + '/' + item, bucket)


 #   count_files(folderpath)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def write_list(localFileName, a_list):

    with open(localFileName, "w", newline="\n") as f:
        for element in a_list:
            f.write("%s\n" % element)


def count_files(folderpath):

    file_count = sum(len(files) for _, _, files in os.walk(folderpath, topdown=True))
    print(file_count)


def get_filenames(folderpath, bucket):

    count = 0

    for(path, dirs, files) in os.walk(folderpath, topdown=True):
#        for filename in fnmatch.filter(files, '*.jpg'):
        for filename in files:
            filepath = os.path.join(path, filename)
            count += 1
#            if count % 10 == 0:
            print(f"{count} {filepath}")

            key = "dev/" + filepath[9:]

 #           save_S3(filepath, bucket, key)


#        for filename in files:
#            if fnmatch.fnmatch(filename, '*.jpeg') or fnmatch.fnmatch(filename, '*.jpg') or fnmatch.fnmatch(filename, '*.png'):
#                filepath = os.path.join(path, filename)
#                count += 1
#                if count % 10 == 0:
#                    print(f"{count} {filepath}")

def save_S3(localFileName, bucketName, keyName):

    s3Client = boto3.client('s3')

    response = s3Client.upload_file(localFileName, bucketName, keyName)
    if response != None:
        print(response)

    return True
