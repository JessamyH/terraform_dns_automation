terraform {
  backend "s3" {
    bucket  = "week6-terraform-state-jessamy"
    key     = "week6/terraform.tfstate"
    region  = "ap-southeast-2"
    encrypt = true
  }
}
