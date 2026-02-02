import boto3
from botocore.exceptions import ClientError

def upsert_record(hosted_zone_id, changes, comment=None):
	"""
	封装 Route 53 UPSERT 操作。
	:param hosted_zone_id: Hosted Zone ID
	:param changes: dict, ResourceRecordSet changes
	:param comment: str, optional comment
	:return: (response, error) tuple
	"""
	route53 = boto3.client("route53")
	try:
		response = route53.change_resource_record_sets(
			HostedZoneId=hosted_zone_id,
			ChangeBatch={
				"Changes": [changes],
				"Comment": comment or "Automated change by Lambda"
			}
		)
		return response, None
	except ClientError as ce:
		return None, ce
