from localstack.utils.aws import aws_models
vaAFm=super
vaAFB=None
vaAFE=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  vaAFm(LambdaLayer,self).__init__(arn)
  self.cwd=vaAFB
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.vaAFE.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,vaAFE,env=vaAFB):
  vaAFm(RDSDatabase,self).__init__(vaAFE,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,vaAFE,env=vaAFB):
  vaAFm(RDSCluster,self).__init__(vaAFE,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,vaAFE,env=vaAFB):
  vaAFm(AppSyncAPI,self).__init__(vaAFE,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,vaAFE,env=vaAFB):
  vaAFm(AmplifyApp,self).__init__(vaAFE,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,vaAFE,env=vaAFB):
  vaAFm(ElastiCacheCluster,self).__init__(vaAFE,env=env)
class TransferServer(BaseComponent):
 def __init__(self,vaAFE,env=vaAFB):
  vaAFm(TransferServer,self).__init__(vaAFE,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,vaAFE,env=vaAFB):
  vaAFm(CloudFrontDistribution,self).__init__(vaAFE,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,vaAFE,env=vaAFB):
  vaAFm(CodeCommitRepository,self).__init__(vaAFE,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
