# Grafana ECS Fargate/ALB variables

variable "grafana_image" {
  description = "Grafana Docker image"
  type        = string
  default     = "grafana/grafana:10.4.2"
}

variable "grafana_port" {
  description = "Grafana container port"
  type        = number
  default     = 3000
}

variable "public_subnet_ids" {
  description = "Public subnet IDs for ALB"
  type        = list(string)
}

variable "vpc_id" {
  description = "VPC ID for all resources"
  type        = string
}

variable "subnet_id" {
  description = "Subnet ID for ECS Fargate"
  type        = string
}

variable "region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "ap-southeast-2"
}
