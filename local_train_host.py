#!/usr/bin/env python3

import sagemaker
import time
from sagemaker.estimator import Estimator
from sagemaker.serializers import JSONSerializer
import boto3


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

# deploy
predictor = estimator.deploy(1, instance_type, wait=True)
print("completed deploy")
time.sleep(5)

# predict
predictor.serializer = JSONSerializer()
#predictor.deserializer = JSONDeserializer
print("running prediction")
prediction = predictor.predict({'my_info': [ "s3 location", "other things.." ]})
print("prediction done")
print("predicted:"+str(prediction))
predictor.delete_endpoint()