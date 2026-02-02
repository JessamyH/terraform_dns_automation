output "hosted_zone_id" {
  value = aws_route53_zone.jessamy_dns_test.zone_id
}

output "base_domain" {
  value = aws_route53_zone.jessamy_dns_test.name
}
