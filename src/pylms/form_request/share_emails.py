"""Helper function to select facilitators for form sharing."""

from ..cli import input_bool, input_menu
from ..cli_utils import parse_nums
from ..config import Config
from ..errors import ForcedExitError, Result


def input_share_emails(config: Config) -> Result[list[str]]:
    """Prompt user to select which facilitators should receive form links.

    Provides interactive menu to select facilitators. Always includes admin email.
    Allows selecting none of the facilitators.

    Args:
        config: Config containing admin and facilitator information.

    Returns:
        Result[list[str]]: List of selected Gmail addresses (always includes admin).
    """
    # Always include admin email
    emails = [config.admin]

    if len(config.facilitators) == 0:
        return Result.ok(emails)

    while True:
        confirm = input_bool("Add facilitator emails?")
        if confirm.is_err() and isinstance(confirm.error, ForcedExitError):
            return confirm.propagate()
        elif confirm.is_err():
            confirm.print_if_err()
            continue

        if not confirm.unwrap():
            break

        # Build facilitator options
        options = [f"{f.name} ({f.gmail})" for f in config.facilitators]
        options.append("None - Don't send to any facilitators")

        # Prompt user to select facilitators
        result = input_menu(
            options,
            prompt="Select facilitators to share form with (admin will always receive it):",
        )

        if result.is_err():
            return result.propagate()

        nums = result.unwrap()

        nums = parse_nums(nums)
        if nums.is_err():
            return nums.propagate()

        indices = nums.unwrap()
        chosen_facilitators = [
            config.facilitators[i] for i in indices if i < len(config.facilitators)
        ]
        chosen_emails = [f.gmail for f in chosen_facilitators]
        emails.extend(chosen_emails)
        break

    return Result.ok(emails)
