import json
import boto3
import io

def lambda_handler(event, context):

    folders = ["signatures", "attachments"]
    bucket = "wishyoo-sih-source"
    keys_to_send = 100
    send_all = False
    test_send_number = 10
    

    sqsURL = "https://sqs.us-west-2.amazonaws.com/727869158831/copy_image_files_EFS_to_S3"

    for folder in folders:
        key = "image_path/dev/" + folder +".txt"

        fileStream = openFilefromS3(bucket, key)
        fileBinary = fileStream.getvalue()

        file_string = str(fileBinary, 'utf-8')
        temp_list = list(file_string.split("\n"))
        folder_list = ['/' + folder + "/" + item for item in temp_list]

        list_length = len(folder_list)

        print(f"{key} {list_length}")

        list_range = int(list_length/keys_to_send)
        if not send_all:
            list_range = test_send_number

        for j in range(list_range):
            message = ""
            for i in range(keys_to_send):
                message += str(folder_list[i+j*keys_to_send]) + ','

            sendMessageSQS(sqsURL, message[:-1])

        if list_length%keys_to_send != 0 and send_all:
            message = ""
            for i in range(list_range*keys_to_send, list_length):
                message += str(folder_list[i]) + ','

            sendMessageSQS(sqsURL, message[:-1])

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def openFilefromS3(bucketName, keyName):

    s3 = boto3.client('s3')
    s3_connection = boto3.resource('s3')

    waiterFlg = s3.get_waiter('object_exists')
    waiterFlg.wait(Bucket=bucketName, Key=keyName)

    s3_object = s3_connection.Object(bucketName,keyName)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())

    return stream


def sendMessageSQS(sqsURL, message):

    sqs = boto3.client('sqs')

    response = sqs.send_message(
        QueueUrl=sqsURL,
        DelaySeconds=10,
        MessageAttributes={
            'Folders': {
                'DataType': 'String',
                'StringValue': str(message)
            }
        },
        MessageBody=(
            str(message)
        )
    )
