variable "hosted_zone_id" {
  description = "Route 53 Hosted Zone ID"
  type        = string
}

variable "base_domain" {
  description = "Base domain for DNS records"
  type        = string
}

variable "lambda_role_arn" {
  description = "Lambda least privilege role ARN"
  type        = string
}
