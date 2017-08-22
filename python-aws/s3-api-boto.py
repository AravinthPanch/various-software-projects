__author__ = 'Aravinth Panchadcharam'
__email__ = "me@aravinth.info"
__date__ = '10/09/15'

import boto.s3.connection

AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""

# Create the connection
# hostname must be adjusted based on the region
conn = boto.connect_s3(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    host='s3.eu-central-1.amazonaws.com',
    is_secure=False,
)


# To get all the bucketss
for meter_bucket in conn.get_all_buckets():
    print meter_bucket.name


# To get a bucket based on bucket name
meter_bucket = conn.get_bucket('meter_bucket')


# To get all the files (keys) in the bucket
meter_files = meter_bucket.list()
for key in meter_files:
    print key.name


# To get a file from the bucket using file(key) name
meter_file_key = meter_bucket.get_key('bucket_file.txt')


# Find only top level folders in the bucket
for meter_folder in meter_bucket.list("", "/"):
    print meter_folder.name
