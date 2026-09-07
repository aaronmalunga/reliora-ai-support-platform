resource "aws_lambda_function" "ticket_execution" {
  function_name = local.ticket_lambda_function_name

  role = aws_iam_role.ticket_lambda.arn

  runtime       = "python3.12"
  architectures = ["x86_64"]

  handler = "reliora.adapters.aws.lambda_entrypoint.lambda_handler"

  filename = abspath(
    "${path.root}/../../../../build/lambda/reliora-ticket-execution.zip"
  )

  source_code_hash = filebase64sha256(
    abspath(
      "${path.root}/../../../../build/lambda/reliora-ticket-execution.zip"
    )
  )

  environment {
    variables = {
      RELIORA_OPERATIONS_TABLE = aws_dynamodb_table.operations.name
      RELIORA_TICKETS_TABLE    = aws_dynamodb_table.tickets.name
    }
  }

  depends_on = [
    aws_cloudwatch_log_group.ticket_lambda,
    aws_iam_role_policy.ticket_lambda_execution,
  ]
}