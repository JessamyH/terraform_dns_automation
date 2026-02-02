resource "aws_sqs_queue" "client_domains_requests_dlq_jessamy" {
  name = "client-domains-requests-dlq-jessamy"
}

resource "aws_sqs_queue" "client_domains_requests_jessamy" {
  name = "client-domains-requests-jessamy"
  visibility_timeout_seconds = 60

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.client_domains_requests_dlq_jessamy.arn
    maxReceiveCount     = 5
  })
}
