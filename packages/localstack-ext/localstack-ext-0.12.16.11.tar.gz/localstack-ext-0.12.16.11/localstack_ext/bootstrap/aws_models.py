from localstack.utils.aws import aws_models
ASkOr=super
ASkOH=None
ASkOE=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  ASkOr(LambdaLayer,self).__init__(arn)
  self.cwd=ASkOH
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.ASkOE.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,ASkOE,env=ASkOH):
  ASkOr(RDSDatabase,self).__init__(ASkOE,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,ASkOE,env=ASkOH):
  ASkOr(RDSCluster,self).__init__(ASkOE,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,ASkOE,env=ASkOH):
  ASkOr(AppSyncAPI,self).__init__(ASkOE,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,ASkOE,env=ASkOH):
  ASkOr(AmplifyApp,self).__init__(ASkOE,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,ASkOE,env=ASkOH):
  ASkOr(ElastiCacheCluster,self).__init__(ASkOE,env=env)
class TransferServer(BaseComponent):
 def __init__(self,ASkOE,env=ASkOH):
  ASkOr(TransferServer,self).__init__(ASkOE,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,ASkOE,env=ASkOH):
  ASkOr(CloudFrontDistribution,self).__init__(ASkOE,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,ASkOE,env=ASkOH):
  ASkOr(CodeCommitRepository,self).__init__(ASkOE,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
