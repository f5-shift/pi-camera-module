import os
from picamera import PiCamera
from argparse import ArgumentParser
import time
#from boto.s3.connection import S3Connection
#from boto.s3.key import Key
import boto3
from datetime import datetime
import json

AWS_ACCESS =''
AWS_SECRET= ''
#REGION_HOST='s3.eu-west-2.amazonaws.com'
#conn=S3Connection(AWS_ACCESS,AWS_SECRET,host=REGION_HOST)
#bucket= conn.get_bucket('f5shift-accelerator-test')
directory=os.getcwd()
bucket_name= 'f5shift-accelerator-test'

s3=boto3.client('s3',
        aws_access_key_id = AWS_ACCESS,
        aws_secret_access_key=AWS_SECRET,
        region_name='eu-west-2')
def upload_S3 (dir, file):
    k=Key(bucket)
    k.key=file
    k.set_contents_from_filename(dir+file)

sleep_timeout = 3

def setup_aws():
    with open('credentials.json') as json_file:
        json_data = json.loads(json_file.read())
        access_key = json_data['AWS_ACCESS']
        secret = json_data['AWS_SECRET']

        s3=boto3.client('s3',
            aws_access_key_id = access_key,
            aws_secret_access_key = secret,
            region_name = 'eu-west-2'
        )

        return s3


if __name__ == "__main__":
    s3 = setup_aws()

    if not s3:
        print("S3 failed to configure")
        exit(-1)

    print("S3 setup correctly")

    with PiCamera() as camera:
        print("camera initialised")
        camera.resolution = 1024, 768

        camera.start_preview()
        for _ in range(5):
            now = datetime.now()
            now_str = now.strftime('%m_%d_%y_%H_%M_%S')

            # prefix filename with now stirng
            filename = now_str + ".jpg"

            camera.capture(filename)
            s3.upload_file(os.path.join(directory, filename), bucket_name, filename)

            print("Uploaded %s successfully" % filename)

            time.sleep(sleep_timeout)

        #response=s3.list_buckets()
        #print(response)

        camera.stop_preview()
        camera.close()
