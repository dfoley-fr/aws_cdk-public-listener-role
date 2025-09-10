import pytest
from aws_cdk import App, Stack
from alb_listener_rule import AlbListenerRuleStack


def test_alb_listener_rule_creation():
    """Test that AlbListenerRuleStack can be created with required parameters."""
    app = App()
    stack = Stack(app, "TestStack")
    
    listener_rule = AlbListenerRuleStack(
        stack, "TestListenerRule",
        target_group_arn="arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/test-tg/1234567890",
        ecs_stack_name="test-ecs-stack",
        listener_priority=100,
        host_name="api.example.com"
    )
    
    assert listener_rule.listener_rule is not None
    assert listener_rule.listener_rule.priority == 100