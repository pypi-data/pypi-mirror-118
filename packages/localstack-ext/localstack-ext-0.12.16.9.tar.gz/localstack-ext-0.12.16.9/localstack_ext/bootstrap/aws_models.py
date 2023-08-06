from localstack.utils.aws import aws_models
cPwCd=super
cPwCb=None
cPwCk=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  cPwCd(LambdaLayer,self).__init__(arn)
  self.cwd=cPwCb
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.cPwCk.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,cPwCk,env=cPwCb):
  cPwCd(RDSDatabase,self).__init__(cPwCk,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,cPwCk,env=cPwCb):
  cPwCd(RDSCluster,self).__init__(cPwCk,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,cPwCk,env=cPwCb):
  cPwCd(AppSyncAPI,self).__init__(cPwCk,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,cPwCk,env=cPwCb):
  cPwCd(AmplifyApp,self).__init__(cPwCk,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,cPwCk,env=cPwCb):
  cPwCd(ElastiCacheCluster,self).__init__(cPwCk,env=env)
class TransferServer(BaseComponent):
 def __init__(self,cPwCk,env=cPwCb):
  cPwCd(TransferServer,self).__init__(cPwCk,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,cPwCk,env=cPwCb):
  cPwCd(CloudFrontDistribution,self).__init__(cPwCk,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,cPwCk,env=cPwCb):
  cPwCd(CodeCommitRepository,self).__init__(cPwCk,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
