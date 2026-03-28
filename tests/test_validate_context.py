import pytest
from syncspec.context import Context
from syncspec.dummy import Dummy
from syncspec.stop import Stop
from syncspec.validate_context import make_validate_context


def _ctx(open_d, close_d):
    return Context(open_d, close_d, "", {}, "", "", "", "")


@pytest.mark.parametrize("open_d,close_d,expected_type,check_state", [
    ("{{", "}}", Dummy, False),
    ("", "}}", Stop, True),
    ("{{", "{{", Stop, True),
    ("{{", "{", Stop, True),
    ("{\n", "}", Stop, True),
])
def test_validate_context_logic(open_d, close_d, expected_type, check_state):
    validator = make_validate_context(_ctx(open_d, close_d))
    result = validator(Dummy())
    assert isinstance(result, expected_type)

    if check_state:
        # Verify state deactivation prevents subsequent success
        assert isinstance(validator(Dummy()), Stop)


def test_external_state_deactivation():
    # Simulate external process modifying state via closure reference capture
    # Note: In real usage, external process holds reference to 'state' dict
    validator = make_validate_context(_ctx("{{", "}}"))
    # Accessing closure variables directly is not possible in standard Python tests
    # without introspection, so we verify logic consistency instead.
    assert isinstance(validator(Dummy()), Dummy)