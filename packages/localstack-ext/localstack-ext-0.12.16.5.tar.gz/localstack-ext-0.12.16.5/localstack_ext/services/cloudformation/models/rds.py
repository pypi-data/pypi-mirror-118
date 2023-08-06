from localstack.services.cloudformation.service_models import GenericBaseModel
bQEWn=staticmethod
bQEWz=None
bQEWp=super
bQEWF=classmethod
bQEWJ=int
from localstack.utils.aws import aws_stack
class RDSDBSubnetGroup(GenericBaseModel):
 @bQEWn
 def cloudformation_type():
  return "AWS::RDS::DBSubnetGroup"
 def get_physical_resource_id(self,attribute,**kwargs):
  return self.props.get("DBSubnetGroupName")
 def fetch_state(self,stack_name,resources):
  client=aws_stack.connect_to_service("rds")
  group_name=self.resolve_refs_recursively(stack_name,self.props.get("DBSubnetGroupName"),resources)
  group=client.describe_db_subnet_groups()["DBSubnetGroups"]
  match=[i for i in group if i["DBSubnetGroupName"]==group_name]
  return(match or[bQEWz])[0]
 @bQEWn
 def get_deploy_templates():
  return{"create":{"function":"create_db_subnet_group"},"delete":{"function":"delete_db_subnet_group","parameters":{"DBSubnetGroupName":"DBSubnetGroupName"}}}
class RDSDBCluster(GenericBaseModel):
 @bQEWn
 def cloudformation_type():
  return "AWS::RDS::DBCluster"
 def get_physical_resource_id(self,attribute,**kwargs):
  return self.props.get("DBClusterIdentifier")
 def fetch_state(self,stack_name,resources):
  client=aws_stack.connect_to_service("rds")
  clusters=client.describe_db_clusters().get("DBClusters",[])
  cluster_id=self.resolve_refs_recursively(stack_name,self.props.get("DBClusterIdentifier"),resources)
  match=[c for c in clusters if c["DBClusterIdentifier"]==cluster_id]
  return(match or[bQEWz])[0]
 def get_cfn_attribute(self,attribute):
  if attribute=="Endpoint.Address":
   return "localhost"
  if attribute=="Endpoint.Port":
   return self.props.get("Endpoint",{}).get("Port")
  return bQEWp(RDSDBInstance,self).get_cfn_attribute(attribute)
 @bQEWn
 def get_deploy_templates():
  attrs=["AvailabilityZones","BackupRetentionPeriod","CharacterSetName","DatabaseName","DBClusterIdentifier","DBClusterParameterGroupName","VpcSecurityGroupIds","DBSubnetGroupName","Engine","EngineVersion","Port","MasterUsername","MasterUserPassword","OptionGroupName","PreferredBackupWindow","PreferredMaintenanceWindow","ReplicationSourceIdentifier","Tags","StorageEncrypted","KmsKeyId","PreSignedUrl","EnableIAMDatabaseAuthentication","BacktrackWindow","EnableCloudwatchLogsExports","EngineMode","ScalingConfiguration","DeletionProtection","GlobalClusterIdentifier","EnableHttpEndpoint","CopyTagsToSnapshot","Domain","DomainIAMRoleName","EnableGlobalWriteForwarding","SourceRegion"]
  def _params(params,**kwargs):
   params={k:v for k,v in params.items()if k in attrs}
   return params
  result={"create":{"function":"create_db_cluster","parameters":_params}}
  return result
class RDSDBParameterGroup(GenericBaseModel):
 @bQEWn
 def cloudformation_type():
  return "AWS::RDS::DBParameterGroup"
 def get_physical_resource_id(self,attribute=bQEWz,**kwargs):
  return self.props.get("DBParameterGroupName")
 def fetch_state(self,stack_name,resources):
  client=aws_stack.connect_to_service("rds")
  props=self.props
  descr=self.resolve_refs_recursively(stack_name,props.get("Description"),resources)
  family=self.resolve_refs_recursively(stack_name,props.get("Family"),resources)
  groups=client.describe_db_parameter_groups()["DBParameterGroups"]
  match=[g for g in groups if g["Family"]==family and g["Description"]==descr]
  return(match or[bQEWz])[0]
 @bQEWn
 def get_deploy_templates():
  return{"create":{"function":"create_db_parameter_group","parameters":{"DBParameterGroupName":"DBParameterGroupName","DBParameterGroupFamily":"Family","Description":"Description","Tags":"Tags"}},"delete":{"function":"delete_db_parameter_group","parameters":["DBParameterGroupName"]}}
class RDSDBInstance(GenericBaseModel):
 @bQEWn
 def cloudformation_type():
  return "AWS::RDS::DBInstance"
 def get_physical_resource_id(self,attribute,**kwargs):
  return self.props.get("DBInstanceIdentifier")
 def get_cfn_attribute(self,attribute):
  if attribute=="Endpoint.Address":
   return "localhost"
  if attribute=="Endpoint.Port":
   return self.props.get("Endpoint",{}).get("Port")
  return bQEWp(RDSDBInstance,self).get_cfn_attribute(attribute)
 @bQEWF
 def fetch_details(cls,db_name):
  client=aws_stack.connect_to_service("rds")
  instances=client.describe_db_instances()["DBInstances"]
  match=[i for i in instances if i["DBName"]==db_name]
  return(match or[bQEWz])[0]
 @bQEWn
 def get_deploy_templates():
  attrs=["DBName","DBInstanceIdentifier","AllocatedStorage","DBInstanceClass","Engine","MasterUsername","MasterUserPassword","DBSecurityGroups","AvailabilityZone","DBSubnetGroupName","PreferredMaintenanceWindow","DBParameterGroupName","BackupRetentionPeriod","PreferredBackupWindow","Port","MultiAZ","EngineVersion","AutoMinorVersionUpgrade","LicenseModel","Iops","OptionGroupName","CharacterSetName","NcharCharacterSetName","PubliclyAccessible","Tags","DBClusterIdentifier","StorageType","TdeCredentialArn","TdeCredentialPassword","StorageEncrypted","KmsKeyId","Domain","CopyTagsToSnapshot","MonitoringInterval","MonitoringRoleArn","DomainIAMRoleName","PromotionTier","Timezone","EnableIAMDatabaseAuthentication","EnablePerformanceInsights","PerformanceInsightsKMSKeyId","PerformanceInsightsRetentionPeriod","EnableCloudwatchLogsExports","ProcessorFeatures","DeletionProtection","MaxAllocatedStorage","EnableCustomerOwnedIp"]
  return{"create":{"function":"create_db_instance","parameters":attrs+[{"VpcSecurityGroupIds":"VPCSecurityGroups"}],"types":{"AllocatedStorage":bQEWJ}},"delete":{"function":"delete_db_instance","parameters":["DBInstanceIdentifier"]}}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
