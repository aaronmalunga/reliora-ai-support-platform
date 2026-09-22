resource "aws_dynamodb_table" "operations" {
  name         = "reliora-${var.environment}-operations"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "operation_id"

  attribute {
    name = "operation_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "tickets" {
  name         = "reliora-${var.environment}-tickets"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "ticket_id"

  attribute {
    name = "ticket_id"
    type = "S"
  }
}