import pytest
from expert_ceylon.matchers.rete import utils


def test_prepare_rule_is_dnf():
    from expert_ceylon import Rule, NOT, AND, OR, Fact
    from expert_ceylon.matchers.rete.dnf import dnf

    rule = Rule(AND(Fact(0), NOT(OR(Fact(1), Fact(2)))))(lambda:None)

    assert list(utils.prepare_rule(rule)) == [Fact(0),
                                              NOT(Fact(1)),
                                              NOT(Fact(2))]


def test_prepare_rule_empty():
    from expert_ceylon import Rule, InitialFact

    rule = Rule()(lambda:None)

    assert list(utils.prepare_rule(rule)) == [InitialFact()]


def test_prepare_rule__rule_starting_with_not():
    from expert_ceylon import Rule, InitialFact, NOT, Fact

    rule = Rule(NOT(Fact(1)))(lambda:None)

    assert list(utils.prepare_rule(rule)) == [InitialFact(), NOT(Fact(1))]


def test_prepare_rule__and_starting_with_not():
    from expert_ceylon import Rule, InitialFact, NOT, Fact, OR, AND

    rule = Rule(OR(Fact(1), AND(NOT(Fact(2)), Fact(3))))(lambda:None)

    assert list(utils.prepare_rule(rule)) == [OR(Fact(1),
                                                 AND(InitialFact(),
                                                     NOT(Fact(2)),
                                                     Fact(3)))]

def test_prepare_rule__and_inside_rule():
    from expert_ceylon import Rule, AND, Fact

    rule = Rule(AND(Fact(1), Fact(2)))(lambda:None)

    assert list(utils.prepare_rule(rule)) == [Fact(1), Fact(2)]


def test_prepare_rule__or_starting_with_not():
    from expert_ceylon import Rule, InitialFact, NOT, Fact, OR, AND

    rule = Rule(OR(NOT(Fact(1)), NOT(Fact(2))))(lambda:None)

    assert list(utils.prepare_rule(rule)) == [OR(AND(InitialFact(),
                                                     NOT(Fact(1))),
                                                 AND(InitialFact(),
                                                     NOT(Fact(2))))]

def test_extract_facts():
    from expert_ceylon import Rule, NOT, AND, OR, Fact

    rule = Rule(OR(AND(Fact(1), NOT(Fact(2))), Fact(3)))

    assert utils.extract_facts(rule) == {Fact(1), Fact(2), Fact(3)}


def test_illegal_CE():
    from expert_ceylon import Rule, KnowledgeEngine
    from expert_ceylon.conditionalelement import ConditionalElement

    class KE(KnowledgeEngine):
        @Rule(ConditionalElement())
        def r1():
            pass

    with pytest.raises(TypeError):
        KE()
