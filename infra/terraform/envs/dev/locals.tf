locals {
  ticket_lambda_function_name = "reliora-${var.environment}-ticket-execution"

  ticket_lambda_log_group_name = "/aws/lambda/${local.ticket_lambda_function_name}"

  ticket_lambda_log_stream_arn = "arn:${data.aws_partition.current.partition}:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:${local.ticket_lambda_log_group_name}:*"
}