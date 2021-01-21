#!/usr/bin/env python3

import sagemaker
from sagemaker.estimator import Estimator
import boto3
import pathlib


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
                      instance_count=1,
                      instance_type=instance_type,
                      image_name='sagemaker-example:latest',
                      hyperparameters=hyper_parameters)
estimator.fit('file://tmp/train-data')
print("trainig completed")

# The location of the test dataset
batch_input = 'file://tmp/batch-data/'
batch_output = 'file://' + str(pathlib.Path().absolute()) + '/tmp/example-output'

print("creating transformer")
transformer = estimator.transformer(instance_count=1,
                                    instance_type=instance_type,
                                    assemble_with='Line',
                                    max_payload=1,
                                    output_path=batch_output)
print("transforming")
transformer.transform(data=batch_input, content_type='text/csv', split_type='Line')
transformer.wait()

print("completed deploy")

