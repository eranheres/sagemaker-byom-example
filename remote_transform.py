#!/usr/bin/env python3

import sagemaker
import boto3
import pprint

pp = pprint.PrettyPrinter(indent=4)

try:
    role = sagemaker.get_execution_role()
except ValueError:
    iam = boto3.client('iam')
    role = iam.get_role(RoleName='sagemaker')['Role']['Arn']

model_name = "sagemaker-example-fixed"

# getting our model information (docker uri and model data)
client = boto3.client('sagemaker')
model_info = client.describe_model(ModelName=model_name)
print(model_info)
pp.pprint(model_info)
image_uri = model_info['PrimaryContainer']['Image']
model_data = model_info['PrimaryContainer']['ModelDataUrl']

# upload batch data for transforming
sess = sagemaker.Session()
BATCH_WORK_DIRECTORY = 'tmp/batch-data'
s3_batch_prefix = 'sagemaker-example/batch-data'
batch_input = sess.upload_data(BATCH_WORK_DIRECTORY, key_prefix=s3_batch_prefix)
model = sagemaker.model.Model(
    image_uri=image_uri,
    model_data=model_data,
    role=role
)

# creating a transormer and transforming
print("creating transformer")
transformer = model.transformer(instance_count=1, instance_type='ml.m4.xlarge')
print("transforming")
transformer.transform(data=batch_input, data_type='S3Prefix', content_type='text/csv', split_type='Line')
print("waiting for termination")
transformer.wait()

