from localstack.utils.aws import aws_models
RzXgs=super
RzXgm=None
RzXgv=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  RzXgs(LambdaLayer,self).__init__(arn)
  self.cwd=RzXgm
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.RzXgv.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,RzXgv,env=RzXgm):
  RzXgs(RDSDatabase,self).__init__(RzXgv,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,RzXgv,env=RzXgm):
  RzXgs(RDSCluster,self).__init__(RzXgv,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,RzXgv,env=RzXgm):
  RzXgs(AppSyncAPI,self).__init__(RzXgv,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,RzXgv,env=RzXgm):
  RzXgs(AmplifyApp,self).__init__(RzXgv,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,RzXgv,env=RzXgm):
  RzXgs(ElastiCacheCluster,self).__init__(RzXgv,env=env)
class TransferServer(BaseComponent):
 def __init__(self,RzXgv,env=RzXgm):
  RzXgs(TransferServer,self).__init__(RzXgv,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,RzXgv,env=RzXgm):
  RzXgs(CloudFrontDistribution,self).__init__(RzXgv,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,RzXgv,env=RzXgm):
  RzXgs(CodeCommitRepository,self).__init__(RzXgv,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
