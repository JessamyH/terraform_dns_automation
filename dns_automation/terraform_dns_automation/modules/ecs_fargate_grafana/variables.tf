variable "project_name" { type = string }
variable "cluster_name" { type = string }
variable "task_family" { type = string }
variable "cpu" { type = string }
variable "memory" { type = string }
variable "container_name" { type = string }
variable "service_name" { type = string }
variable "desired_count" { type = number }
variable "subnets" { type = list(string) }
variable "security_groups" { type = list(string) }
variable "target_group_arn" { type = string }
variable "region" { type = string }
variable "grafana_image" { type = string }
variable "grafana_port" { type = number }

variable "task_role_arn" { type = string }
