"""Provisioning must fail closed without current protected trial evidence."""

from datetime import date

import pytest

from scripts.azure.preflight import validate_target, validate_trial


@pytest.mark.parametrize(
    "policy", [{}, {"spendingLimit": "Off"}, {"spendingLimit": "CurrentPeriodOff"}]
)
def test_unprotected_trial_is_rejected(policy):
    with pytest.raises(ValueError, match="spending"):
        validate_trial(
            {"state": "Enabled", "subscriptionPolicies": policy}, "2026-10-20", date(2026, 10, 13)
        )


def test_protected_unexpired_trial_is_allowed():
    validate_trial(
        {"state": "Enabled", "subscriptionPolicies": {"spendingLimit": "On"}},
        "2026-10-20",
        date(2026, 10, 13),
    )


@pytest.mark.parametrize("today", [date(2026, 10, 20), date(2026, 10, 21)])
def test_expired_trial_is_rejected(today):
    with pytest.raises(ValueError, match="expired"):
        validate_trial(
            {"state": "Enabled", "subscriptionPolicies": {"spendingLimit": "On"}},
            "2026-10-20",
            today,
        )


def test_disabled_subscription_is_rejected():
    with pytest.raises(ValueError, match="Enabled"):
        validate_trial(
            {"state": "Disabled", "subscriptionPolicies": {"spendingLimit": "On"}},
            "2026-10-20",
            date(2026, 10, 13),
        )


@pytest.mark.parametrize(
    "actual,expected,group",
    [
        ("other", "expected", "medkb-azure-demo-test"),
        ("expected", "expected", "production"),
        ("", "", "medkb-azure-demo-test"),
        ("expected", "expected", "medkb-azure-demo-"),
    ],
)
def test_wrong_or_ambiguous_target_is_rejected(actual, expected, group):
    with pytest.raises(ValueError):
        validate_target(actual, expected, group)


def test_exact_demo_target_is_allowed():
    validate_target(
        "670958af-a1c1-4b8a-8fc9-0aa868ff8b44",
        "670958af-a1c1-4b8a-8fc9-0aa868ff8b44",
        "medkb-azure-demo-test",
    )
