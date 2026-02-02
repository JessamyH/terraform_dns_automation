resource "aws_cloudwatch_log_group" "grafana" {
  name              = "/ecs/grafana"
  retention_in_days = 7
}
provider "aws" {
  region = "ap-southeast-2"
}

module "sqs" {
  source = "./modules/sqs"
}

module "route53" {
  source = "./modules/route53"
}

module "client_domains_lambda" {
  source          = "./modules/lambda"
  hosted_zone_id  = module.route53.hosted_zone_id
  base_domain     = module.route53.base_domain
  lambda_role_arn = module.iam.lambda_role_arn
}

module "iam" {
  source = "./modules/iam"
}

resource "aws_lambda_event_source_mapping" "sqs_to_lambda_jessamy" {
  event_source_arn = module.sqs.queue_arn
  function_name    = module.client_domains_lambda.function_name
  enabled          = true
  batch_size       = 1
}

# --- Security Groups ---
module "security_group" {
  source = "./modules/security_group"
  vpc_id = var.vpc_id
}

# --- ALB ---
module "alb" {
  source            = "./modules/alb"
  vpc_id            = var.vpc_id
  public_subnet_ids = var.public_subnet_ids
  alb_sg_id         = module.security_group.alb_sg_id
}

# --- ECS Fargate Grafana ---
module "ecs_fargate_grafana" {
  source           = "./modules/ecs_fargate_grafana"
  project_name     = "grafana-fargate-demo"
  cluster_name     = "grafana-ecs-cluster"
  task_family      = "grafana-task"
  cpu              = "512"
  memory           = "1024"
  container_name   = "grafana"
  service_name     = "grafana-service"
  desired_count    = 1
  subnets          = [var.subnet_id]
  security_groups  = [module.security_group.ecs_sg_id]
  target_group_arn = module.alb.tg_arn
  region           = var.region
  grafana_image    = var.grafana_image
  grafana_port     = var.grafana_port
  task_role_arn    = module.iam.grafana_task_role_arn
}

// NAT Gateway, EIP, Route Table, and association for private subnet
resource "aws_eip" "nat_eip" {}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = var.public_subnet_ids[0]
  tags = {
    Name = "natgw-jessamy"
  }
}

resource "aws_route_table" "private" {
  vpc_id = var.vpc_id
  tags = {
    Name = "rtb-private-jessamy"
  }
}

resource "aws_route" "private_nat" {
  route_table_id         = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat.id
}

resource "aws_route_table_association" "private_subnet" {
  subnet_id      = var.subnet_id
  route_table_id = aws_route_table.private.id
}
