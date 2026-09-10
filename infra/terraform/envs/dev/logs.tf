resource "aws_cloudwatch_log_group" "ticket_lambda" {
  name              = local.ticket_lambda_log_group_name
  retention_in_days = 7
}