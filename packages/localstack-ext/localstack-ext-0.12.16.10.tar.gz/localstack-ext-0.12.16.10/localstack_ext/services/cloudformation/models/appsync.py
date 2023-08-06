import json
TuEge=staticmethod
TuEgm=classmethod
TuEgv=None
TuEgP=True
TuEgW=hasattr
TuEgH=Exception
TuEgk=super
from localstack.services.cloudformation.service_models import(REF_ARN_ATTRS,REF_ID_ATTRS,GenericBaseModel)
from localstack.utils.aws import aws_stack
from localstack.utils.common import clone,keys_to_lower,to_str
from localstack_ext.services.appsync import appsync_api
from localstack_ext.services.cloudformation.service_models import LOG
from localstack_ext.utils.aws import aws_utils
class AppSyncResolver(GenericBaseModel):
 @TuEge
 def cloudformation_type():
  return "AWS::AppSync::Resolver"
 def get_physical_resource_id(self,attribute,**kwargs):
  if attribute in REF_ID_ATTRS:
   return self.props.get("resolverArn")
 def fetch_state(self,stack_name,resources):
  props=self.props
  api_id=props.get("ApiId")
  type_name=props.get("TypeName")
  field_name=props.get("FieldName")
  data_source_name=props.get("DataSourceName")
  return self.fetch_details(api_id,type_name,field_name,data_source_name)
 @TuEgm
 def fetch_details(cls,api_id,type_name,field_name,data_source_name):
  client=aws_stack.connect_to_service("appsync")
  resolvers=client.list_resolvers(apiId=api_id,typeName=type_name)["resolvers"]
  result=[r for r in resolvers if r.get("fieldName")==field_name and r.get("dataSourceName")==data_source_name]
  return(result or[TuEgv])[0]
 def get_deploy_templates():
  def get_resolver_params(params,**kwargs):
   params=keys_to_lower(clone(params))
   req_template=params.pop("requestMappingTemplateS3Location",TuEgv)
   res_template=params.pop("responseMappingTemplateS3Location",TuEgv)
   if req_template:
    tmpl=aws_utils.download_s3_object(req_template,as_str=TuEgP)
    if tmpl:
     params["requestMappingTemplate"]=tmpl
   if res_template:
    tmpl=aws_utils.download_s3_object(res_template,as_str=TuEgP)
    if tmpl:
     params["responseMappingTemplate"]=tmpl
   return params
  return{"create":{"function":"create_resolver","parameters":get_resolver_params}}
class GraphQLSchema(GenericBaseModel):
 @TuEge
 def cloudformation_type():
  return "AWS::AppSync::GraphQLSchema"
 def get_physical_resource_id(self,attribute,**kwargs):
  return "%s-GraphQLSchema"%self.props.get("ApiId")
 @TuEgm
 def fetch_details(cls,api_id,definition=TuEgv,s3_location=TuEgv):
  client=aws_stack.connect_to_service("appsync")
  try:
   schema=client.get_introspection_schema(apiId=api_id,format="SDL")["schema"]
   schema=schema.read()if TuEgW(schema,"read")else schema
   schema=to_str(schema)
   if schema.startswith("{"):
    schema=json.loads(schema)["schema"]
   if definition:
    if to_str(definition).strip()==to_str(schema).strip():
     return{"schema":definition}
   elif s3_location:
    LOG.debug("Getting GraphQL schema definition from S3 not yet implemented")
    return{"schema":definition}
  except TuEgH:
   pass
class AppSyncApiKey(GenericBaseModel):
 @TuEge
 def cloudformation_type():
  return "AWS::AppSync::ApiKey"
 def get_cfn_attribute(self,attribute_name):
  props=self.props
  if attribute_name=="ApiKey":
   return "key-%s"%props["ApiId"]
  if attribute_name in REF_ID_ATTRS:
   key_id=props.get("ApiKeyId")or props.get("id")
   return aws_utils.appsync_api_key_arn(props.get("ApiId"),key_id)
  return TuEgk(AppSyncApiKey,self).get_cfn_attribute(attribute_name)
 def fetch_state(self,stack_name,resources):
  props=self.props
  api_id=props.get("ApiId")
  api_id=self.resolve_refs_recursively(stack_name,api_id,resources)
  keys=aws_stack.connect_to_service("appsync").list_api_keys(apiId=api_id)["apiKeys"]
  result=[k for k in keys if k.get("description")==props.get("Description")and k.get("expires")==props.get("Expires")]
  return(result or[TuEgv])[0]
 @TuEge
 def get_deploy_templates():
  result={"create":{"function":"create_api_key","parameters":{"apiId":"ApiId","description":"Description","expires":"Expires"}}}
  return result
class AppSyncDataSource(GenericBaseModel):
 @TuEge
 def cloudformation_type():
  return "AWS::AppSync::DataSource"
 @TuEge
 def get_deploy_templates():
  def lambda_get_datasource_config(params,**kwargs):
   params=keys_to_lower(clone(params))
   if params.get("dynamoDBConfig"):
    params["dynamodbConfig"]=params.pop("dynamoDBConfig")
   return params
  return{"create":{"function":"create_data_source","parameters":lambda_get_datasource_config}}
 def fetch_state(self,stack_name,resources):
  props=self.props
  client=aws_stack.connect_to_service("appsync")
  ds_name=props.get("Name")or self.resource_id
  ds_name=self.resolve_refs_recursively(stack_name,ds_name,resources)
  api_id=self.resolve_refs_recursively(stack_name,props.get("ApiId"),resources)
  sources=client.list_data_sources(apiId=api_id)["dataSources"]
  return([s for s in sources if s["name"]==ds_name]or[TuEgv])[0]
class AppSyncFunctionConfig(GenericBaseModel):
 @TuEge
 def cloudformation_type():
  return "AWS::AppSync::FunctionConfiguration"
 def fetch_state(self,stack_name,resources):
  client=aws_stack.connect_to_service("appsync")
  props=self.props
  api_id=self.resolve_refs_recursively(stack_name,props["ApiId"],resources)
  name=self.resolve_refs_recursively(stack_name,props["Name"],resources)
  result=client.list_functions(apiId=api_id).get("functions",[])
  result=[f for f in result if f.get("name")==name]
  return(result or[TuEgv])[0]
 def get_cfn_attribute(self,attribute_name):
  props=self.props
  if attribute_name=="FunctionId":
   return props.get("functionArn","").split("functions/")[-1]
  if attribute_name=="FunctionArn":
   return props.get("functionArn")
  if attribute_name=="Name":
   return props.get("name")
  if attribute_name=="DataSourceName":
   return props.get("dataSourceName")
  return TuEgk(AppSyncFunctionConfig,self).get_cfn_attribute(attribute_name)
 def get_physical_resource_id(self,attribute,**kwargs):
  return self.props.get("functionArn")
 @TuEge
 def get_deploy_templates():
  def func_params(params,**kwargs):
   sys_cfg=params.get("SyncConfig")
   if sys_cfg:
    sys_cfg=keys_to_lower(clone(sys_cfg))
   result={"apiId":"ApiId","name":"Name","description":"Description","dataSourceName":"DataSourceName","requestMappingTemplate":"RequestMappingTemplate","responseMappingTemplate":"ResponseMappingTemplate","functionVersion":"FunctionVersion","syncConfig":sys_cfg}
   result={k:params.get(v)for k,v in result.items()if params.get(v)}
   return result
  return{"create":{"function":"create_function","parameters":func_params}}
class GraphQLAPI(GenericBaseModel):
 @TuEge
 def cloudformation_type():
  return "AWS::AppSync::GraphQLApi"
 def get_cfn_attribute(self,attribute_name):
  props=self.props
  if not props.get("apiId"):
   details=self.fetch_details(props.get("Name"))
   if not details:
    raise TuEgH('Unable to find GraphQL API named "%s"'%props.get("Name"))
   props["apiId"]=details["apiId"]
  if attribute_name=="ApiId":
   return props.get("apiId")
  if attribute_name in REF_ARN_ATTRS:
   return self.get_physical_resource_id(attribute_name)
  if attribute_name=="GraphQLUrl":
   return appsync_api.get_graphql_url(props["apiId"],use_domain_name=TuEgP)
  return TuEgk(GraphQLAPI,self).get_cfn_attribute(attribute_name)
 def get_physical_resource_id(self,attribute,**kwargs):
  props=self.props
  return props.get("apiId")and aws_utils.appsync_api_arn(props["apiId"])
 @TuEgm
 def fetch_details(cls,api_name):
  client=aws_stack.connect_to_service("appsync")
  apis=client.list_graphql_apis()["graphqlApis"]
  return([a for a in apis if a["name"]==api_name]or[TuEgv])[0]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
