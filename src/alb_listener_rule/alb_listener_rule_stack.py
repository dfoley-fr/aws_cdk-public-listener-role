from aws_cdk import (
    aws_elasticloadbalancingv2 as elbv2,
    Stack,
    Fn,
    CfnOutput,
)
from constructs import Construct
class AlbListenerRuleStack(Construct):
    def __init__(
            self, scope: Construct, construct_id: str, *,
            target_group_arn: str,
            ecs_stack_name: str,
            listener_priority: int, 
            host_name: str,  
            **kwargs
        ):
        super().__init__(scope, construct_id, **kwargs)

        listener_arn = Fn.import_value(
            Fn.sub("${ECSStackName}-ALBListenerHTTPS", {
                "ECSStackName": ecs_stack_name
            })
        )

        # Create the listener rule
        listener_rule = elbv2.CfnListenerRule(
            self, "AlbListenerRule",
            listener_arn=listener_arn,
            priority=listener_priority,
            conditions=[
                elbv2.CfnListenerRule.RuleConditionProperty(
                    field="host-header",
                    values=[host_name]
                )
            ],
            actions=[
                elbv2.CfnListenerRule.ActionProperty(
                    type="forward",
                    target_group_arn=target_group_arn
                )
            ],
        )
        # Outputs
        CfnOutput(
            self, "AlbListenerRuleArn",
            value=listener_rule.ref,
            export_name=f"{Stack.of(self).stack_name}-AlbListenerRuleArn",
            description="ARN of the created ALB listener rule"
        )
        CfnOutput(
            self, "AlbListenerRulePriority",
            value=str(listener_rule.priority),
            export_name=f"{Stack.of(self).stack_name}-AlbListenerRulePriority",
            description="Priority of the created ALB listener rule"
        )