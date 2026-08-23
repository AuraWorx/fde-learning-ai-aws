import os
import json
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigatewayv2 as apigw,
    aws_apigatewayv2_integrations as apigw_int,
    aws_apigateway as apigateway,
    aws_stepfunctions as sf,
    aws_iam as iam,
    aws_logs as _logs,
)
from constructs import Construct

LAMBDA_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "lambda")
)

class simpleagent(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        decied_tool_fn = _lambda.Function(
            self, "decide_toolFuntion",
            function_name= "decide_tool",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="decide_tool.handler",
            code=_lambda.Code.from_asset(LAMBDA_DIR),
            timeout=cdk.Duration.seconds(30),
            environment={"BEDROCK_MODEL": "us.anthropic.claude-haiku-4-5-20251001-v1:0"},
        )
        decied_tool_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
            resources=["*"]
        ))

        fetch_data_fn = _lambda.Function(
            self, "fetch_dataFunction",
            function_name= "fetch_data",
            runtime = _lambda.Runtime.PYTHON_3_11,
            handler="fetch_data.handler",
            code=_lambda.Code.from_asset(LAMBDA_DIR),
            timeout=cdk.Duration.seconds(30),
            environment={"BEDROCK_MODEL": "us.anthropic.claude-haiku-4-5-20251001-v1:0"},
        )

        synthesize_fn = _lambda.Function(
            self, "SynthesizeFunction",
            function_name = "synthesize",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="synthesize.handler",
            code=_lambda.Code.from_asset(LAMBDA_DIR),
            timeout=cdk.Duration.seconds(60),
            environment={"BEDROCK_MODEL": "us.anthropic.claude-haiku-4-5-20251001-v1:0"},
        )
        synthesize_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["bedrock:InvokeModel"],
            resources=["*"]
        ))

        statemachine_log_group = _logs.LogGroup(self,"SimpleAgent_StateMachine_Logs")

        state_machine_fn = sf.StateMachine(
            self, "SimpleAgentStateMachine",
            definition_body=sf.DefinitionBody.from_file(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "simple_agent", "state_machine.json")
                ),
            state_machine_type = sf.StateMachineType.EXPRESS,
            timeout=cdk.Duration.minutes(5),
            logs = sf.LogOptions(
                destination = statemachine_log_group,
                level = sf.LogLevel.ALL,
                include_execution_data=True
            )
        )
        state_machine_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["lambda:InvokeFunction"],
            resources=["*"]
        ))

        # api = apigw.HttpApi(self,"SimpleAgentAPI")
        # api.add_routes(
        #     path="/simpleagent",
        #     methods=[apigw.HttpMethod.POST],
        #     integration=apigw_int.HttpStepFunctionsIntegration(
        #         "StartAgentRun",
        #         state_machine=state_machine_fn,
        #         subtype=apigw.HttpIntegrationSubtype.STEPFUNCTIONS_START_SYNC_EXECUTION,
        #         parameter_mapping=apigw.ParameterMapping()
        #             .custom("Input", "$request.body")
        #             .custom("StateMachineArn", state_machine_fn.state_machine_arn),
        #     ),)

        step_functions_role = iam.Role(
            self, "ApiGatewayStepFunctionsRole",
            assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com")
        )
        step_functions_role.add_to_policy(iam.PolicyStatement(
            actions=["states:StartSyncExecution"],
            resources=[state_machine_fn.state_machine_arn]
        ))

        api = apigateway.RestApi(self, "SimpleAgentRestAPI")
        simpleagent_resource = api.root.add_resource("simpleagent")
        simpleagent_resource.add_method(
            "POST",
            apigateway.AwsIntegration(
                service="states",
                action="StartSyncExecution",
                integration_http_method="POST",
                options=apigateway.IntegrationOptions(
                    credentials_role=step_functions_role,
                    request_templates={
                        "application/json": json.dumps({
                            "input": "$util.escapeJavaScript($input.json('$'))",
                            "stateMachineArn": state_machine_fn.state_machine_arn
                        })
                    },
                    integration_responses=[
                        apigateway.IntegrationResponse(
                            status_code="200",
                            response_templates={
                                "application/json": (
                                    "#set($inputRoot = $input.path('$'))\n"
                                    "#set($output = $util.parseJson($inputRoot.output))\n"
                                    "$output.answer"
                                )
                            }
                        )
                    ]
                )
            ),
            method_responses=[apigateway.MethodResponse(status_code="200")]
        )

        

        # api = apigw.RestApi(self, "AIAPI",
        #     rest_api_name="Forward Deployed AI API",
        #     description="Serverless AI API with Bedrock integration."
        # )

        # chat = api.root.add_resource("chat")
        # chat_integration = apigw.LambdaIntegration(decied_tool_fn, proxy=True)
        # chat.add_method("POST", chat_integration)

        # summarize = api.root.add_resource("summarize")
        # summarize_integration = apigw.LambdaIntegration(synthesize_fn, proxy=True)
        # summarize.add_method("POST", summarize_integration)

        cdk.CfnOutput(self, "APIUrl", value=api.url)

app = cdk.App()
simpleagent(app, "simpleagent")
app.synth()

