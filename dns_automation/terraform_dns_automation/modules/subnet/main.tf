resource "aws_subnet" "public" {
  vpc_id                  = var.vpc_id
  cidr_block              = var.cidr_block
  map_public_ip_on_launch = true
  availability_zone       = var.az
  tags = {
    Name = var.name
  }
}

output "subnet_id" {
  value = aws_subnet.public.id
}
