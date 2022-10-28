# Criando uma role
resource "aws_im_role" "lambda" {
    name = "DiLambdaRole"

    assume_role_poicy = <<EOF
{
        "Version": "2012-10-17",
        "Statment": [
        {
            "Acion": "sts:AssumeRole",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": "AssumeRole"
        }
    ]
}
EOF

   tags = {
    IES = "IGTI"
    CURSO = "EDC"
   }
}

# Criando uma policy
resource "aws_iam_policy" "lambda" {
    name = "DiAWSLambdaBasicExecutionRolePolicy"
    path = "/"
    description = "Provides write permissions to ClodWatch Logs, S3 buckets and EMR Steps"

    policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "elasticmapreduce:*"
            ],
            "Resource": "*"
        },
        {
            "Action": "iam:PassRole",
            "Resource": ["arn:aws:iam::127012818163:role/EMR_DefaultRole",
                         "arn:aws:iam::127012818163:role/EMR_EC2_DefaultRole"],
            "Effect": "Allow"
        }
    ]
}
EOF
}

# Realizando vinculação das policies e das roles
resource "aws_iam_role_policy_attatchment" "lambda_attach" {
    role       = aws_iam_role.lambda.name
    policy_arn = aws_iam_policy.lambda.arn
}
