from localstack.utils.aws import aws_models
aObIs=super
aObIu=None
aObID=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  aObIs(LambdaLayer,self).__init__(arn)
  self.cwd=aObIu
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.aObID.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,aObID,env=aObIu):
  aObIs(RDSDatabase,self).__init__(aObID,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,aObID,env=aObIu):
  aObIs(RDSCluster,self).__init__(aObID,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,aObID,env=aObIu):
  aObIs(AppSyncAPI,self).__init__(aObID,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,aObID,env=aObIu):
  aObIs(AmplifyApp,self).__init__(aObID,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,aObID,env=aObIu):
  aObIs(ElastiCacheCluster,self).__init__(aObID,env=env)
class TransferServer(BaseComponent):
 def __init__(self,aObID,env=aObIu):
  aObIs(TransferServer,self).__init__(aObID,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,aObID,env=aObIu):
  aObIs(CloudFrontDistribution,self).__init__(aObID,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,aObID,env=aObIu):
  aObIs(CodeCommitRepository,self).__init__(aObID,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
