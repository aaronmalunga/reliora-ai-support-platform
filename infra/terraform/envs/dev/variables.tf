variable "aws_region" {
  description = "AWS region for the Reliora development environment."
  type        = string
  default     = "us-east-1"

  validation {
    condition     = var.aws_region == "us-east-1"
    error_message = "Reliora P1-S2 development infrastructure must use us-east-1."
  }
}

variable "environment" {
  description = "Deployment environment represented by this Terraform root module."
  type        = string
  default     = "dev"

  validation {
    condition     = var.environment == "dev"
    error_message = "This Terraform root module represents the Reliora dev environment."
  }
}