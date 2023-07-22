# lambda用のiamロールを定義
resource "aws_iam_role" "lambda" {
  name               = "${var.prefix}-role-for-lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda.json
  inline_policy {
    name   = "${var.prefix}-inline-policy-for-lambda"
    policy = data.aws_iam_policy_document.inline_lambda.json
  }
}

# lambda用のiamロールにマネージドポリシーをアタッチ
resource "aws_iam_role_policy_attachment" "lambda_execution_role" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# eventbridge用のiamロールを定義
resource "aws_iam_role" "eventbridge_scheduler" {
  name               = "${var.prefix}-role-for-eventbridge"
  assume_role_policy = data.aws_iam_policy_document.assume_eventbridge_scheduler.json
  inline_policy {
    name   = "${var.prefix}-inline-policy-for-eventbridge"
    policy = data.aws_iam_policy_document.inline_eventbridge_scheduler.json
  }
}
