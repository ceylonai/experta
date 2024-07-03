import pytest


def test_node_exists():
    try:
        from expert_ceylon.matchers.rete.abstract import Node
        from expert_ceylon.matchers.rete.abstract import OneInputNode
        from expert_ceylon.matchers.rete.abstract import TwoInputNode
    except ImportError as exc:
        assert False, exc


def test_node_interface():
    from expert_ceylon.matchers.rete.abstract import Node

    assert {'_reset', 'add_child'} <= Node.__abstractmethods__


def test_oneinputnode_interface():
    from expert_ceylon.matchers.rete.abstract import OneInputNode

    assert {'_activate'} <= OneInputNode.__abstractmethods__


def test_twoinputnode_interface():
    from expert_ceylon.matchers.rete.abstract import TwoInputNode

    assert {'_activate_left',
            '_activate_right'} <= TwoInputNode.__abstractmethods__
