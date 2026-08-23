import os
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
)
from constructs import Construct

LAMBDA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lambda")

class AIServerlessStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        chat_fn = _lambda.Function(
            self, "ChatFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="chat.handler",
            code=_lambda.Code.from_asset(LAMBDA_DIR),
            timeout=cdk.Duration.seconds(30),
            environment={"BEDROCK_MODEL": "us.anthropic.claude-haiku-4-5-20251001-v1:0"},
        )
        chat_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
            resources=["*"]
        ))

        summarize_fn = _lambda.Function(
            self, "SummarizeFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="summarize.handler",
            code=_lambda.Code.from_asset(LAMBDA_DIR),
            timeout=cdk.Duration.seconds(60),
            environment={"BEDROCK_MODEL": "us.anthropic.claude-haiku-4-5-20251001-v1:0"},
        )
        summarize_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["bedrock:InvokeModel"],
            resources=["*"]
        ))

        api = apigw.RestApi(self, "AIAPI",
            rest_api_name="Forward Deployed AI API",
            description="Serverless AI API with Bedrock integration."
        )

        chat = api.root.add_resource("chat")
        chat_integration = apigw.LambdaIntegration(chat_fn, proxy=True)
        chat.add_method("POST", chat_integration)

        summarize = api.root.add_resource("summarize")
        summarize_integration = apigw.LambdaIntegration(summarize_fn, proxy=True)
        summarize.add_method("POST", summarize_integration)

        cdk.CfnOutput(self, "APIUrl", value=api.url)

app = cdk.App()
AIServerlessStack(app, "AIServerlessStack")
app.synth()
