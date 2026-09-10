provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project          = "Reliora"
      PortfolioProject = "P1-S2"
      Environment      = var.environment
      ManagedBy        = "Terraform"
    }
  }
}

data "aws_caller_identity" "current" {}

data "aws_partition" "current" {}