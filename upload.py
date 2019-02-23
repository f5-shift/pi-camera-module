import os
from picamera import PiCamera
from argparse import ArgumentParser
import time
#from boto.s3.connection import S3Connection
#from boto.s3.key import Key
import boto3

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

if __name__ == "__main__":
    ap = ArgumentParser()
    ap.add_argument('output')

    args = ap.parse_args()
    with PiCamera() as camera:
        camera.resolution = 1024, 768
        camera.start_preview()

        time.sleep(2)

        camera.capture(args.output)
        s3.upload_file(os.path.join(directory,args.output), bucket_name, args.output)
        #response=s3.list_buckets()
        #print(response)
