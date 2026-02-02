resource "aws_iam_role" "grafana_task_role" {
  name = "grafana-task-role-jessamy"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = { Service = "ecs-tasks.amazonaws.com" },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "grafana_cloudwatch" {
  name        = "grafana-cloudwatch-access-jessamy"
  description = "Allow Grafana ECS task to access CloudWatch metrics and logs"
  policy      = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "cloudwatch:ListMetrics",
          "cloudwatch:GetMetricData",
          "logs:DescribeLogGroups",
          "logs:GetLogEvents",
          "logs:FilterLogEvents",
          "logs:StartQuery",
          "logs:GetQueryResults",
          "logs:GetLogGroupFields"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "grafana_cloudwatch_attach" {
  role       = aws_iam_role.grafana_task_role.name
  policy_arn = aws_iam_policy.grafana_cloudwatch.arn
}

resource "aws_iam_role" "ecs_grafana_task_execution" {
  name = "ecs-grafana-task-exec-role-jessamy"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = { Service = "ecs-tasks.amazonaws.com" },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_grafana_task_exec_policy" {
  role       = aws_iam_role.ecs_grafana_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

