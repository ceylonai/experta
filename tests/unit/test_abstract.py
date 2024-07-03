import pytest


def test_matcher_exists():
    try:
        from expert_ceylon.abstract import Matcher
    except ImportError as exc:
        assert False, exc


def test_matcher_interface():
    from expert_ceylon.abstract import Matcher

    assert Matcher.__abstractmethods__ == {'changes', 'reset'}
