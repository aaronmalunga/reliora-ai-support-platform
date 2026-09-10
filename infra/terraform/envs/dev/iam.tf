data "aws_iam_policy_document" "ticket_lambda_assume_role" {
  statement {
    sid    = "AllowLambdaServiceAssumeRole"
    effect = "Allow"

    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type = "Service"

      identifiers = [
        "lambda.amazonaws.com",
      ]
    }
  }
}

resource "aws_iam_role" "ticket_lambda" {
  name = "reliora-${var.environment}-ticket-execution"

  assume_role_policy = data.aws_iam_policy_document.ticket_lambda_assume_role.json
}

data "aws_iam_policy_document" "ticket_lambda_execution" {
  statement {
    sid    = "ReadOperationState"
    effect = "Allow"

    actions = [
      "dynamodb:GetItem",
    ]

    resources = [
      aws_dynamodb_table.operations.arn,
    ]
  }

  statement {
    sid    = "WriteTicketTransaction"
    effect = "Allow"

    actions = [
      "dynamodb:PutItem",
    ]

    resources = [
      aws_dynamodb_table.operations.arn,
      aws_dynamodb_table.tickets.arn,
    ]

    condition {
      test     = "ForAnyValue:StringEquals"
      variable = "dynamodb:EnclosingOperation"

      values = [
        "TransactWriteItems",
      ]
    }
  }

  statement {
    sid    = "WriteLambdaLogs"
    effect = "Allow"

    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = [
      local.ticket_lambda_log_stream_arn,
    ]
  }
}

resource "aws_iam_role_policy" "ticket_lambda_execution" {
  name = "reliora-${var.environment}-ticket-execution"

  role   = aws_iam_role.ticket_lambda.id
  policy = data.aws_iam_policy_document.ticket_lambda_execution.json
}