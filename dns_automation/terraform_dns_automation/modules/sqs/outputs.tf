output "queue_url" {
  value = aws_sqs_queue.client_domains_requests_jessamy.id
}

output "queue_arn" {
  value = aws_sqs_queue.client_domains_requests_jessamy.arn
}
