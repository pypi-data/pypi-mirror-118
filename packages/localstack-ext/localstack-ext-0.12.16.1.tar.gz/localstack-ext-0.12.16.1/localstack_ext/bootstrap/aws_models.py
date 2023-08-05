from localstack.utils.aws import aws_models
ENfVa=super
ENfVw=None
ENfVY=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  ENfVa(LambdaLayer,self).__init__(arn)
  self.cwd=ENfVw
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.ENfVY.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,ENfVY,env=ENfVw):
  ENfVa(RDSDatabase,self).__init__(ENfVY,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,ENfVY,env=ENfVw):
  ENfVa(RDSCluster,self).__init__(ENfVY,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,ENfVY,env=ENfVw):
  ENfVa(AppSyncAPI,self).__init__(ENfVY,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,ENfVY,env=ENfVw):
  ENfVa(AmplifyApp,self).__init__(ENfVY,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,ENfVY,env=ENfVw):
  ENfVa(ElastiCacheCluster,self).__init__(ENfVY,env=env)
class TransferServer(BaseComponent):
 def __init__(self,ENfVY,env=ENfVw):
  ENfVa(TransferServer,self).__init__(ENfVY,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,ENfVY,env=ENfVw):
  ENfVa(CloudFrontDistribution,self).__init__(ENfVY,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,ENfVY,env=ENfVw):
  ENfVa(CodeCommitRepository,self).__init__(ENfVY,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
