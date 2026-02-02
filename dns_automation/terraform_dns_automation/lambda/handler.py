def handler(event, context):
    import json
    from datetime import datetime
    
    # SQS event format: event["Records"][0]["body"]
    try:
        record = event["Records"][0]
        body = record["body"]
        data = json.loads(body)
    except Exception as e:
        error_log = {
            "status": "failure",
            "error_type": "InvalidJSON",
            "error_message": str(e),
            "body": event.get("Records", [{}])[0].get("body", str(event))
        }
        print(json.dumps(error_log, default=str))
        return error_log

    # Safe handling of metadata field
    metadata = data.get("metadata", {})

    # Structured log output
    log = {
        "request_id": data.get("request_id"),
        "action": data.get("action"),
        "client": data.get("client"),
        "subdomain": data.get("subdomain"),
        "target_domain": data.get("target"),
        "status": "success",
        "metadata": metadata,
        "timestamp": datetime.utcnow().isoformat(),
    }
    print(json.dumps(log))
    return {"status": "ok"}
