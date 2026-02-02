output "lambda_function_name" {
  value       = module.client_domains_lambda.function_name
  description = "Lambda function name"
}

output "lambda_function_arn" {
  value       = module.client_domains_lambda.function_arn
  description = "Lambda function ARN"
}

output "sqs_queue_url" {
  value       = module.sqs.queue_url
  description = "SQS queue URL"
}

output "route53_zone_id" {
  value       = module.route53.hosted_zone_id
  description = "Route 53 Hosted Zone ID"
}

output "route53_base_domain" {
  value       = module.route53.base_domain
  description = "Route 53 base domain name"
}

output "grafana_alb_dns" {
  value = module.alb.alb_dns_name
}
