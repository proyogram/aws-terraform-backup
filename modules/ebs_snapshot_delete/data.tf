# lambdaソースをzip化してupload
data "archive_file" "archieve_lambda" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_src"
  output_path = "${path.module}/lambda_src_zip/lambda.zip"
}

# policy関連のdata
data "aws_iam_policy_document" "assume_lambda" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}
data "aws_iam_policy_document" "inline_lambda" {
  statement {
    actions = [
      "ec2:DescribeImages",
			"ec2:DescribeSnapshots",
			"ec2:DeleteSnapshot"
    ]
    resources = ["*"]
  }
}


data "aws_iam_policy_document" "assume_eventbridge_scheduler" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type = "Service"
      identifiers = [
        "scheduler.amazonaws.com",
      ]
    }
  }
}

data "aws_iam_policy_document" "inline_eventbridge_scheduler" {
  statement {
    effect = "Allow"

    actions = [
      "lambda:InvokeFunction",
    ]

    resources = [
      "*",
    ]
  }
}