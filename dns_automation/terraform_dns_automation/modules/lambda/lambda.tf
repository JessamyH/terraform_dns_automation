resource "aws_lambda_function" "client_domains" {
  function_name = "client-domains-lambda-jessamy"
  filename      = "lambda.zip" # You need to package main.py and dependencies first
  handler       = "main.handler"
  runtime       = "python3.11"
  role          = var.lambda_role_arn

  environment {
    variables = {
      HOSTED_ZONE_ID = var.hosted_zone_id
      BASE_DOMAIN    = var.base_domain
    }
  }
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_route53" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonRoute53FullAccess"
}
