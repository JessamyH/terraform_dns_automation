output "grafana_task_role_arn" {
  value = aws_iam_role.grafana_task_role.arn
  description = "ECS Fargate Grafana Task Role ARN"
}
output "lambda_role_arn" {
  value = aws_iam_role.lambda_jessamy.arn
  description = "Lambda least privilege role ARN"
}

output "ecs_grafana_task_execution_role_arn" {
  value = aws_iam_role.ecs_grafana_task_execution.arn
  description = "ECS Fargate Grafana Task Execution Role ARN"
}