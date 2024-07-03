import pytest

from hypothesis import strategies as st
from hypothesis import assume, settings
from hypothesis.database import DirectoryBasedExampleDatabase
from hypothesis.stateful import Bundle, RuleBasedStateMachine, rule, invariant, consumes

from expert_ceylon.activation import Activation
from expert_ceylon.agenda import Agenda
from expert_ceylon.engine import KnowledgeEngine
from expert_ceylon.fact import Fact
from expert_ceylon.factlist import FactList
from expert_ceylon.rule import Rule
from expert_ceylon.strategies import DepthStrategy


def get_rule_stm(strategy):
    class StrategyStateMachine(RuleBasedStateMachine):
        def __init__(self):
            super(StrategyStateMachine, self).__init__()
            self.model = set()
            self.agenda = Agenda()
            self.strategy = strategy()
            self.fss = set()

        activations = Bundle("activations")

        @rule(target=activations,
              r=st.integers(min_value=0),
              fs=st.sets(st.integers(min_value=0), min_size=1))
        def declare(self, r, fs):
            assume((r, frozenset(fs)) not in self.fss)
            self.fss.add((r, frozenset(fs)))

            fs = [Fact(i, __factid__=i) for i in fs]
            act = Activation(Rule(Fact(r)), facts=tuple(fs))

            # Update agenda
            self.strategy.update_agenda(self.agenda, [act], [])

            # Update model
            self.model |= set([act])

            return act

        @rule(act=consumes(activations))
        def retract(self, act):
            # Update agenda
            self.strategy.update_agenda(self.agenda, [], [act])

            # Update model
            self.model -= set([act])

        @invariant()
        def values_agree(self):
            assert set(self.agenda.activations) == self.model

    return StrategyStateMachine


test_depthstrategy_state_machine = get_rule_stm(DepthStrategy).TestCase
