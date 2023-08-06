from localstack.utils.aws import aws_models
awWFE=super
awWFM=None
awWFK=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  awWFE(LambdaLayer,self).__init__(arn)
  self.cwd=awWFM
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.awWFK.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,awWFK,env=awWFM):
  awWFE(RDSDatabase,self).__init__(awWFK,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,awWFK,env=awWFM):
  awWFE(RDSCluster,self).__init__(awWFK,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,awWFK,env=awWFM):
  awWFE(AppSyncAPI,self).__init__(awWFK,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,awWFK,env=awWFM):
  awWFE(AmplifyApp,self).__init__(awWFK,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,awWFK,env=awWFM):
  awWFE(ElastiCacheCluster,self).__init__(awWFK,env=env)
class TransferServer(BaseComponent):
 def __init__(self,awWFK,env=awWFM):
  awWFE(TransferServer,self).__init__(awWFK,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,awWFK,env=awWFM):
  awWFE(CloudFrontDistribution,self).__init__(awWFK,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,awWFK,env=awWFM):
  awWFE(CodeCommitRepository,self).__init__(awWFK,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
