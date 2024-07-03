import pytest


def test_deffacts_module_exists():
    try:
        from expert_ceylon import deffacts
    except ImportError as exc:
        assert False, exc


def test_deffacts_class_exists():
    from expert_ceylon import deffacts

    assert hasattr(deffacts, 'DefFacts')


def test_deffacts_can_decorate_generator():
    from expert_ceylon import DefFacts, Fact

    @DefFacts()
    def mygenerator():
        yield Fact()

    assert list(mygenerator()) == [Fact()]


def test_deffacts_return_copies_of_facts():
    from expert_ceylon import DefFacts, Fact

    f0 = Fact()

    @DefFacts()
    def mygenerator():
        yield f0

    assert list(mygenerator())[0] is not f0


def test_deffacts_stores_order():
    from expert_ceylon import DefFacts, Fact

    @DefFacts(order=-10)
    def mygenerator():
        yield Fact()

    assert mygenerator.order == -10


def test_deffacts_does_not_accept_non_generators():
    from expert_ceylon import DefFacts, Fact

    with pytest.raises(TypeError):
        @DefFacts()
        def mygenerator():
            return Fact()


def test_deffacts_can_decorate_methods():
    from expert_ceylon import DefFacts, Fact

    class Test:
        @DefFacts()
        def mygenerator(self):
            yield Fact()

    t = Test()
    assert list(t.mygenerator()) == [Fact()]


def test_deffacts_without_parenthesis():
    from expert_ceylon import DefFacts

    with pytest.raises(SyntaxError):
        @DefFacts
        def mygenerator(self):
            yield Fact()
