provider "aws" {
  region = "ap-northeast-1"
}

terraform {
  required_version = ">= 1.4.0"
  backend "s3" {
    bucket         = "tf-backend-proyogram"
    region         = "ap-northeast-1"
    key            = "backup/terraform.tfstate"
    encrypt        = true
  }
}
