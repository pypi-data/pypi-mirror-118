import json
cKDtx=staticmethod
cKDtI=str
cKDtq=None
cKDti=int
cKDtB=Exception
cKDtT=list
from localstack import config
from localstack.services.awslambda import lambda_executors
from localstack.services.cloudformation.service_models import GenericBaseModel
from localstack.utils.aws import aws_stack
from localstack.utils.common import retry,short_uid,to_str
from localstack.utils.testutil import map_all_s3_objects
from localstack_ext.services.cloudformation.service_models import(CUSTOM_RESOURCE_STATUSES,CUSTOM_RESOURCES_RESULT_POLL_TIMEOUT,CUSTOM_RESOURCES_RESULTS_BUCKET,LOG)
from localstack_ext.utils.aws import aws_utils
class CDKMetadata(GenericBaseModel):
 @cKDtx
 def cloudformation_type():
  return "AWS::CDK::Metadata"
 def fetch_state(self,stack_name,resources):
  return{"type":"AWS::CDK::Metadata"}
class CustomResource(GenericBaseModel):
 @cKDtx
 def cloudformation_type():
  return "AWS::CloudFormation::CustomResource"
 def fetch_state(self,stack_name,resources):
  resource_id=self.logical_resource_id
  result=(CUSTOM_RESOURCE_STATUSES.get(aws_stack.get_region(),{}).get(stack_name,{}).get(resource_id))
  return result
 def get_physical_resource_id(self,attribute,**kwargs):
  return self.logical_resource_id
 @cKDtx
 def get_deploy_templates():
  def create_custom_resource(resource_id,resources,resource_type,func,stack_name,*args):
   resource=resources[resource_id]
   resource_props=resource["Properties"]
   service_token=resource_props.get("ServiceToken")
   if not service_token:
    LOG.warning("Missing ServiceToken attribute in custom resource: %s"%resource)
    return
   s3_client=aws_stack.connect_to_service("s3")
   s3_client.create_bucket(Bucket=CUSTOM_RESOURCES_RESULTS_BUCKET)
   result_key=short_uid()
   main_endpoint=lambda_executors.get_main_endpoint_from_container()
   endpoint_url="http://%s:%s"%(main_endpoint,config.EDGE_PORT_HTTP or config.EDGE_PORT)
   response_url=aws_stack.generate_presigned_url("put_object",Params={"Bucket":CUSTOM_RESOURCES_RESULTS_BUCKET,"Key":result_key},endpoint_url=endpoint_url)
   stack_arn=aws_stack.cloudformation_stack_arn(stack_name)
   request={"RequestType":"Create","ResponseURL":response_url,"StackId":stack_arn,"RequestId":short_uid(),"ResourceType":resource.get("Type"),"LogicalResourceId":resource_id,"ResourceProperties":resource_props}
   if cKDtI(service_token).startswith("arn:aws:lambda"):
    region_name=service_token.split(":")[3]
    function_name=aws_stack.lambda_function_name(service_token)
    lambda_client=aws_stack.connect_to_service("lambda",region_name=region_name)
    lambda_client.invoke(FunctionName=function_name,Payload=json.dumps(request))
   else:
    LOG.warning("Unsupported ServiceToken attribute in custom resource: %s"%service_token)
    return
   def fetch_result():
    return aws_utils.download_s3_object(CUSTOM_RESOURCES_RESULTS_BUCKET,result_key)
   result=cKDtq
   try:
    result=retry(fetch_result,retries=cKDti(CUSTOM_RESOURCES_RESULT_POLL_TIMEOUT/2),sleep=2)
    result=json.loads(to_str(result))
   except cKDtB:
    bucket_objects=map_all_s3_objects(buckets=[CUSTOM_RESOURCES_RESULTS_BUCKET])
    LOG.info("Unable to fetch CF custom resource result from s3://%s/%s . Existing keys: %s"%(CUSTOM_RESOURCES_RESULTS_BUCKET,result_key,cKDtT(bucket_objects.keys())))
    raise
   region=aws_stack.get_region()
   status=CUSTOM_RESOURCE_STATUSES[region]=CUSTOM_RESOURCE_STATUSES.get(region,{})
   status_stack=status[stack_name]=status.get(stack_name,{})
   status_stack[resource_id]={"result":result}
   return result
  return{"create":{"function":create_custom_resource}}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
