import pytest
from aws_cdk import App, Stack, Template
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
    
    # Test that the construct was created successfully
    assert listener_rule is not None
    assert listener_rule.node.id == "TestListenerRule"


def test_alb_listener_rule_template():
    """Test that the CloudFormation template contains the expected resources."""
    app = App()
    stack = Stack(app, "TestStack")
    
    AlbListenerRuleStack(
        stack, "TestListenerRule",
        target_group_arn="arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/test-tg/1234567890",
        ecs_stack_name="test-ecs-stack",
        listener_priority=100,
        host_name="api.example.com"
    )
    
    # Generate CloudFormation template
    template = Template.from_stack(stack)
    
    # Check that a listener rule is created
    template.has_resource_properties("AWS::ElasticLoadBalancingV2::ListenerRule", {
        "Priority": 100,
        "Conditions": [
            {
                "Field": "host-header",
                "Values": ["api.example.com"]
            }
        ]
    })