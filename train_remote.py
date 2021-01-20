#!/usr/bin/env python3

import sagemaker
import boto3
import sys
from sagemaker.estimator import Estimator
import sagemaker as sage

try:
    role = sagemaker.get_execution_role()
except ValueError:
    iam = boto3.client('iam')
    role = iam.get_role(RoleName='sagemaker')['Role']['Arn']

sess = sage.Session()
WORK_DIRECTORY = 'tmp/example-data'

# upload data to S3
s3_prefix = 'sagemaker-example'
data_location = sess.upload_data(WORK_DIRECTORY, key_prefix=s3_prefix)
client = boto3.client('sts')
account = client.get_caller_identity()['Account']

my_session = boto3.session.Session()
region = my_session.region_name

algorithm_name = 'sagemaker-example'

ecr_image = '{}.dkr.ecr.{}.amazonaws.com/{}:latest'.format(account, region, algorithm_name)

print(ecr_image)

hyperparameters = {'train-steps': 100}

instance_type = 'ml.m4.xlarge'

estimator = Estimator(role=role,
                      image_uri=ecr_image,
                      train_instance_count=1,
                      train_instance_type=instance_type,
                      hyperparameters=hyperparameters)

estimator.fit(data_location)

sys.exit(0)
try:
    role = sagemaker.get_execution_role()
except ValueError:
    iam = boto3.client('iam')
    role = iam.get_role(RoleName='sagemaker')['Role']['Arn']

# train
hyper_parameters = {'train-steps': 1}
instance_type = 'local'
estimator = Estimator(role=role,
                      image_uri='sagemaker-example:latest',
                      train_instance_count=1,
                      train_instance_type=instance_type,
                      image_name='sagemaker-example:latest',
                      hyperparameters=hyper_parameters)
estimator.fit('file://tmp/example-data')

# deploy
predictor = estimator.deploy(1, instance_type, wait=True)
print("completed deploy")
time.sleep(5)

# predict
predictor.serializer = json_serializer
print("running prediction")
predictor.predict({'my_info': [ "s3 location", "other things.." ]})
print("predicted")
predictor.delete_endpoint()