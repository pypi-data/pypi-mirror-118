from localstack.utils.aws import aws_models
FmWSf=super
FmWSB=None
FmWSd=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  FmWSf(LambdaLayer,self).__init__(arn)
  self.cwd=FmWSB
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.FmWSd.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,FmWSd,env=FmWSB):
  FmWSf(RDSDatabase,self).__init__(FmWSd,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,FmWSd,env=FmWSB):
  FmWSf(RDSCluster,self).__init__(FmWSd,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,FmWSd,env=FmWSB):
  FmWSf(AppSyncAPI,self).__init__(FmWSd,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,FmWSd,env=FmWSB):
  FmWSf(AmplifyApp,self).__init__(FmWSd,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,FmWSd,env=FmWSB):
  FmWSf(ElastiCacheCluster,self).__init__(FmWSd,env=env)
class TransferServer(BaseComponent):
 def __init__(self,FmWSd,env=FmWSB):
  FmWSf(TransferServer,self).__init__(FmWSd,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,FmWSd,env=FmWSB):
  FmWSf(CloudFrontDistribution,self).__init__(FmWSd,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,FmWSd,env=FmWSB):
  FmWSf(CodeCommitRepository,self).__init__(FmWSd,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
