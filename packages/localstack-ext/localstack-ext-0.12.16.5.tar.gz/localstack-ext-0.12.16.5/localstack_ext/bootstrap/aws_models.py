from localstack.utils.aws import aws_models
imQAg=super
imQAV=None
imQAk=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  imQAg(LambdaLayer,self).__init__(arn)
  self.cwd=imQAV
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.imQAk.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,imQAk,env=imQAV):
  imQAg(RDSDatabase,self).__init__(imQAk,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,imQAk,env=imQAV):
  imQAg(RDSCluster,self).__init__(imQAk,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,imQAk,env=imQAV):
  imQAg(AppSyncAPI,self).__init__(imQAk,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,imQAk,env=imQAV):
  imQAg(AmplifyApp,self).__init__(imQAk,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,imQAk,env=imQAV):
  imQAg(ElastiCacheCluster,self).__init__(imQAk,env=env)
class TransferServer(BaseComponent):
 def __init__(self,imQAk,env=imQAV):
  imQAg(TransferServer,self).__init__(imQAk,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,imQAk,env=imQAV):
  imQAg(CloudFrontDistribution,self).__init__(imQAk,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,imQAk,env=imQAV):
  imQAg(CodeCommitRepository,self).__init__(imQAk,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
