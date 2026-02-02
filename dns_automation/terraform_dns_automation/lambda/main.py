import uuid

import json
import logging
import os
import boto3
from botocore.exceptions import ClientError
from route53_utils import upsert_record

def handler(event, context):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    
    # Log the received event
    logger.info(json.dumps({
        "event": "received",
        "raw_event": event
    }, default=str))
    
    # Set your hosted zone ID here or use an environment variable
    HOSTED_ZONE_ID = os.environ.get("HOSTED_ZONE_ID", "ZXXXXXXXXXXXXXX") 

    for record in event.get('Records', []):
        try:
            body = record.get('body')
            logger.info(json.dumps({
                "event": "processing_record",
                "body": body
            }, default=str))
            # Parse JSON
            try:
                message = json.loads(body)
            except Exception as e:
                logger.error(json.dumps({
                    "request_id": None,
                    "action": None,
                    "client": None,
                    "subdomain": None,
                    "target_domain": None,
                    "status": "failure",
                    "error_type": "InvalidJSON",
                    "error_message": str(e),
                    "body": body
                }, default=str))
                continue

            # Validation rules
            errors = []
            request_id = message.get("request_id")
            if not request_id:
                request_id = str(uuid.uuid4())
                message["request_id"] = request_id


            action = message.get("action")
            subdomain = message.get("subdomain")
            BASE_DOMAIN = "jessamy-dns-test.com"
            client = None
            env = None
            target_env = "production"
            target_domain = None

            # Only validate that subdomain must be production for update and delete actions
            if action in ("update", "delete"):
                if subdomain and subdomain.endswith(BASE_DOMAIN):
                    parts = subdomain.split('.')
                    if len(parts) >= 3:
                        client = parts[0]
                        env = parts[1]
                        if env != "production":
                            errors.append("Only production subdomain can be updated or deleted.")
                        target_domain = subdomain
                    else:
                        target_domain = subdomain
                else:
                    client = message.get("client")
                    env = message.get("env")
                    target_domain = f"{client}.production.{BASE_DOMAIN}" if client else None
            else:
                # add operation is compatible with the original logic
                if subdomain and subdomain.endswith(BASE_DOMAIN):
                    parts = subdomain.split('.')
                    if len(parts) >= 3:
                        client = parts[0]
                        env = parts[1]
                        # If env is staging, automatically convert to production
                        if env == "staging":
                            target_domain = f"{client}.production.{BASE_DOMAIN}"
                        else:
                            target_domain = subdomain
                    else:
                        target_domain = subdomain
                else:
                    client = message.get("client")
                    env = message.get("env")
                    target_domain = f"{client}.production.{BASE_DOMAIN}" if client else None

            # Compatible with old message format
            message["client"] = client
            message["env"] = env
            message["target_env"] = target_env
            message["target_domain"] = target_domain


            # Required fields (ttl is now optional, will default if missing)
            for field in ["action", "subdomain", "target", "record_type"]:
                if field not in message:
                    errors.append(f"Missing required field: {field}")

            # Set default TTL if not provided
            if "ttl" not in message or message["ttl"] in (None, ""):
                message["ttl"] = 300  # default to 300 seconds


            # action must be "add", "update", or "delete"
            if message.get("action") not in ("add", "update", "delete"):
                errors.append("'action' must be 'add', 'update', or 'delete'")

            # record_type must be "A" or "CNAME"
            if message.get("record_type") not in ("A", "CNAME"):
                errors.append("'record_type' must be 'A' or 'CNAME'")


            # ttl must be a positive number
            try:
                ttl = int(message.get("ttl", 0))
                if ttl <= 0:
                    errors.append("'ttl' must be a positive number")
            except Exception:
                errors.append("'ttl' must be a positive number")

            # client, env, target must be non-empty
            for field in ["client", "env", "target"]:
                if not message.get(field):
                    errors.append(f"'{field}' must be non-empty")

            if errors:
                logger.error(json.dumps({
                    "request_id": request_id,
                    "action": action,
                    "client": client,
                    "subdomain": subdomain,
                    "target_domain": None,
                    "status": "failure",
                    "error_type": "ValidationFailed",
                    "error_message": "; ".join(errors),
                    "body": body
                }, default=str))
                continue


            # Log printing, including all key fields
            logger.info(json.dumps({
                "request_id": request_id,
                "action": action,
                "client": client,
                "env": env,
                "target_env": target_env,
                "subdomain": subdomain,
                "target_domain": target_domain,
                "status": "validated"
            }, default=str))


            # Route 53 action mapping

            record_type = message["record_type"]
            ttl = int(message["ttl"])
            target = message["target"]
            action_type = message["action"]
            if action_type in ("add", "update"):
                route53_action = "UPSERT"
            elif action_type == "delete":
                route53_action = "DELETE"
            else:
                route53_action = "UPSERT"  # fallback, should not happen due to validation

            changes = {
                "Action": route53_action,
                "ResourceRecordSet": {
                    "Name": target_domain,
                    "Type": record_type,
                    "TTL": ttl,
                }
            }
            if record_type in ("A", "CNAME"):
                changes["ResourceRecordSet"]["ResourceRecords"] = [{"Value": target}]

            response, error = upsert_record(
                hosted_zone_id=HOSTED_ZONE_ID,
                changes=changes,
                comment=f"Automated {route53_action} for {client} by Lambda"
            )
            if error is None:
                # Log the original message for reference
                logger.info(json.dumps({"original_message": message}, default=str))
                # Print success information
                print("successful")
                print(json.dumps({
                    "request_id": request_id,
                    "action": action_type,
                    "client": client,
                    "subdomain": subdomain,
                    "target_domain": target_domain,
                    "target": target,
                    "record_type": record_type,
                    "status": "success",
                    "error_type": None,
                    "error_message": None,
                    "route53_response": response,
                    "metadata": message.get("metadata", {})
                }, default=str))
            else:
                logger.error(json.dumps({
                    "request_id": request_id,
                    "action": action_type,
                    "client": client,
                    "subdomain": subdomain,
                    "target_domain": target_domain,
                    "status": "failure",
                    "error_type": "Route53ClientError",
                    "error_message": str(error),
                    "metadata": message.get("metadata", {})
                }, default=str))
        except Exception as e:
            logger.error(json.dumps({
                "request_id": None,
                "action": None,
                "client": None,
                "subdomain": None,
                "target_domain": None,
                "status": "failure",
                "error_type": "UnhandledException",
                "error_message": str(e),
                "record": record
            }, default=str))
