#!/usr/bin/env python3

import sagemaker
import boto3
import time
from sagemaker.estimator import Estimator
import sagemaker as sage
from sagemaker.predictor import json_serializer

try:
    role = sagemaker.get_execution_role()
except ValueError:
    iam = boto3.client('iam')
    role = iam.get_role(RoleName='sagemaker')['Role']['Arn']

sess = sage.Session()

# upload train data to S3
TRAIN_WORK_DIRECTORY = 'tmp/train-data'
s3_prefix = 'sagemaker-example'
data_location = sess.upload_data(TRAIN_WORK_DIRECTORY, key_prefix=s3_prefix)
print("train data location {}".format(data_location))
client = boto3.client('sts')
account = client.get_caller_identity()['Account']

# train model
my_session = boto3.session.Session()
region = my_session.region_name
algorithm_name = 'sagemaker-example'
ecr_image = '{}.dkr.ecr.{}.amazonaws.com/{}:latest'.format(account, region, algorithm_name)
print(ecr_image)
hyperparameters = {'train-steps': 3}
instance_type = 'ml.m4.xlarge'
estimator = Estimator(role=role,
                      image_uri=ecr_image,
                      instance_count=1,
                      instance_type=instance_type,
                      hyperparameters=hyperparameters)
estimator.fit(data_location)

# transform batch data
BATCH_WORK_DIRECTORY = 'tmp/train-data'
s3_prefix = 'sagemaker-example'
batch_input = sess.upload_data(BATCH_WORK_DIRECTORY, key_prefix=s3_prefix)
print("input data at"+str(batch_input))
batch_output = ''
print("creating transformer")
exit(0)
transformer = estimator.transformer(instance_count=1, instance_type='ml.m4.xlarge')
print("transforming")
transformer.transform(data=batch_input, data_type='S3Prefix', content_type='text/csv', split_type='Line')
print("waiting for termination")
transformer.wait()