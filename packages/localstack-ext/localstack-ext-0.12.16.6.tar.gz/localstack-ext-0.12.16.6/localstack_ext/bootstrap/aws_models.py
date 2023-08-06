from localstack.utils.aws import aws_models
IGHvc=super
IGHvO=None
IGHvf=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  IGHvc(LambdaLayer,self).__init__(arn)
  self.cwd=IGHvO
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.IGHvf.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,IGHvf,env=IGHvO):
  IGHvc(RDSDatabase,self).__init__(IGHvf,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,IGHvf,env=IGHvO):
  IGHvc(RDSCluster,self).__init__(IGHvf,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,IGHvf,env=IGHvO):
  IGHvc(AppSyncAPI,self).__init__(IGHvf,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,IGHvf,env=IGHvO):
  IGHvc(AmplifyApp,self).__init__(IGHvf,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,IGHvf,env=IGHvO):
  IGHvc(ElastiCacheCluster,self).__init__(IGHvf,env=env)
class TransferServer(BaseComponent):
 def __init__(self,IGHvf,env=IGHvO):
  IGHvc(TransferServer,self).__init__(IGHvf,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,IGHvf,env=IGHvO):
  IGHvc(CloudFrontDistribution,self).__init__(IGHvf,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,IGHvf,env=IGHvO):
  IGHvc(CodeCommitRepository,self).__init__(IGHvf,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
