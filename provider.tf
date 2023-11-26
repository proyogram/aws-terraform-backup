provider "aws" {
  region = "ap-northeast-1"
}

terraform {
  required_version = ">= 1.3.0"
  backend "s3" {
    bucket  = "tf-backend-proyogram"
    region  = "ap-northeast-1"
    key     = "backup/terraform.tfstate"
    encrypt = true
  }
}
