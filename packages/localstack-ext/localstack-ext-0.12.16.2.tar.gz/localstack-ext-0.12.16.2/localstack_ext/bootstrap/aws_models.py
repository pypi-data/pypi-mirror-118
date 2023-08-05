from localstack.utils.aws import aws_models
Ckutr=super
Ckutz=None
CkutG=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  Ckutr(LambdaLayer,self).__init__(arn)
  self.cwd=Ckutz
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.CkutG.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,CkutG,env=Ckutz):
  Ckutr(RDSDatabase,self).__init__(CkutG,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,CkutG,env=Ckutz):
  Ckutr(RDSCluster,self).__init__(CkutG,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,CkutG,env=Ckutz):
  Ckutr(AppSyncAPI,self).__init__(CkutG,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,CkutG,env=Ckutz):
  Ckutr(AmplifyApp,self).__init__(CkutG,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,CkutG,env=Ckutz):
  Ckutr(ElastiCacheCluster,self).__init__(CkutG,env=env)
class TransferServer(BaseComponent):
 def __init__(self,CkutG,env=Ckutz):
  Ckutr(TransferServer,self).__init__(CkutG,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,CkutG,env=Ckutz):
  Ckutr(CloudFrontDistribution,self).__init__(CkutG,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,CkutG,env=Ckutz):
  Ckutr(CodeCommitRepository,self).__init__(CkutG,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
