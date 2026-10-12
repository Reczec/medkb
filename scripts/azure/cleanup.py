"""Preview only by default; delete only an exactly confirmed marked demo group."""

import argparse

from scripts.azure.preflight import az_json, validate_target


def validate_cleanup_target(
    subscription: str,
    expected_subscription: str,
    resource_group: str,
    expected_resource_group: str,
) -> None:
    validate_target(subscription, expected_subscription, resource_group)
    if resource_group != expected_resource_group:
        raise ValueError("Resource group does not match the explicit expected target")


def cleanup_group(
    subscription: str,
    expected_subscription: str,
    resource_group: str,
    expected_resource_group: str,
    *,
    delete: bool,
) -> None:
    validate_cleanup_target(
        subscription, expected_subscription, resource_group, expected_resource_group
    )
    account = az_json(["account", "show", "--subscription", subscription])
    validate_cleanup_target(
        account.get("id", ""), expected_subscription, resource_group, expected_resource_group
    )
    group = az_json(["group", "show", "--subscription", subscription, "--name", resource_group])
    if group.get("tags", {}).get("project") != "medkb-azure-demo":
        raise ValueError("Refusing to delete an unmarked resource group")
    resources = az_json(
        ["resource", "list", "--subscription", subscription, "--resource-group", resource_group]
    )
    print(f"Preview: {resource_group}; {len(resources)} resource(s)")
    for resource in resources:
        print(f"  {resource['type']}: {resource['name']}")
    if not delete:
        print("Preview only. No resources deleted.")
        return
    if (
        input("Type the exact demo resource group to confirm permanent deletion: ")
        != resource_group
    ):
        raise ValueError("Exact typed confirmation required; no resources deleted")
    az_json(["group", "delete", "--subscription", subscription, "--name", resource_group, "--yes"])
    print("Demo group deletion finished; inspect Azure costs for delayed charges.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in (
        "subscription",
        "expected-subscription",
        "resource-group",
        "expected-resource-group",
    ):
        parser.add_argument(f"--{name}", required=True)
    parser.add_argument("--delete", action="store_true")
    args = parser.parse_args()
    try:
        cleanup_group(
            args.subscription,
            args.expected_subscription,
            args.resource_group,
            args.expected_resource_group,
            delete=args.delete,
        )
    except (ValueError, EOFError, OSError):
        parser.exit(1, "Cleanup blocked/failed; no unconfirmed deletion was requested.\n")


if __name__ == "__main__":
    main()
