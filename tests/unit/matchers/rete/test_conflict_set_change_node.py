import pytest


def test_conflictsetchange_exists():
    try:
        from expert_ceylon.matchers.rete.nodes import ConflictSetNode
    except ImportError as exc:
        assert False, exc


def test_conflictsetchange_is_abstractnode():
    from expert_ceylon.matchers.rete.nodes import ConflictSetNode
    from expert_ceylon.matchers.rete.abstract import OneInputNode

    assert issubclass(ConflictSetNode, OneInputNode)


def test_conflictsetchange_interface():
    from expert_ceylon.matchers.rete.nodes import ConflictSetNode

    assert hasattr(ConflictSetNode, 'get_activations')


def test_conflictsetchange_accepts_rule():
    from expert_ceylon.matchers.rete.nodes import ConflictSetNode
    from expert_ceylon.rule import Rule

    # MUST NOT RAISE
    ConflictSetNode(Rule())

    with pytest.raises(TypeError):
        ConflictSetNode('NOTARULE')


def test_conflictsetchange_valid_adds_to_memory():
    from expert_ceylon.fact import Fact
    from expert_ceylon.matchers.rete.nodes import ConflictSetNode
    from expert_ceylon.matchers.rete.token import Token, TokenInfo
    from expert_ceylon.rule import Rule

    csn = ConflictSetNode(Rule())

    f = Fact(test='data')
    f.__factid__ = 1

    csn.activate(Token.valid(f, {'mycontextdata': 'data'}))

    assert TokenInfo([f], {'mycontextdata': 'data'}) in csn.memory


def test_conflictsetchange_invalid_removes_from_memory():
    from expert_ceylon.fact import Fact
    from expert_ceylon.matchers.rete.nodes import ConflictSetNode
    from expert_ceylon.matchers.rete.token import Token, TokenInfo
    from expert_ceylon.rule import Rule

    csn = ConflictSetNode(Rule())

    f = Fact(test='data')
    f.__factid__ = 1

    csn.memory.add(TokenInfo([f], {'mycontextdata': 'data'}))

    csn.activate(Token.invalid(f, {'mycontextdata': 'data'}))

    assert not csn.memory


def test_conflictsetchange_get_activations_data():
    from expert_ceylon.matchers.rete.nodes import ConflictSetNode
    from expert_ceylon.matchers.rete.token import Token
    from expert_ceylon.rule import Rule
    from expert_ceylon.fact import Fact

    rule = Rule()
    csn = ConflictSetNode(rule)

    f = Fact(first=1)
    f.__factid__ = 1

    csn.activate(Token.valid(f, {'data': 'test'}))

    added, removed = csn.get_activations()

    assert len(added) == 1
    assert len(removed) == 0

    assert list(added)[0].rule is rule
    assert f in list(added)[0].facts
    assert list(added)[0].context == {'data': 'test'}
