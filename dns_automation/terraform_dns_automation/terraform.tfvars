
grafana_image = "jessamy/grafana-custom:v1.0.0"
grafana_port  = 3000

# VPC and Subnet configuration for Grafana/ALB
public_subnet_ids = [
  "subnet-0a05dfbfa9b02eb45", # Sample-subnet-public1-ap-southeast-2a
  "subnet-044bb7e2c10d0b1ee"  # Sample-subnet-public2
]
vpc_id    = "vpc-0a775837570253930"    # Sample VPC
subnet_id = "subnet-089bf9a6ed97aad05" # Sample-subnet-private1-ap-southeast-2a


