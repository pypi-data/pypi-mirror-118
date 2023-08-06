"""Helpers to interact with the config file."""
import os

import yaml

VALID_CAPABILITIES = [
    "CAPABILITY_IAM",
    "CAPABILITY_NAMED_IAM",
    "CAPABILITY_AUTO_EXPAND",
]


class Config:
    def __init__(self, stacks):
        self.stacks = stacks

    def get_stack(self, name):
        stack = self.stacks.get(name)
        if stack is None:
            raise Exception(f"Could not find stack config named '{name}'")

        return stack


def parse_stack(section, root, aws_profile, aws_region):
    stack_name = section.get("stack")
    stack_file = section.get("file")
    use_changesets = section.get("use_changesets")
    config_profile = section.get("aws_profile")
    config_region = section.get("aws_region")
    capabilities = section.get("capabilities", [])

    if not os.path.isabs(stack_file):
        stack_file = os.path.join(root, stack_file)

    if not os.path.exists(stack_file):
        raise Exception(f"Could not find stack file: '{stack_file}'")

    if not isinstance(capabilities, list):
        raise Exception("Wrong format for capabilities, expecting list")

    capabilities = set(capabilities)
    if not capabilities.issubset(VALID_CAPABILITIES):
        raise Exception(
            f"Some capabilities are not valid; valid values are '{VALID_CAPABILITIES}'"
        )

    selected_profile = aws_profile or config_profile
    selected_region = aws_region or config_region

    return (
        stack_name,
        stack_file,
        use_changesets,
        capabilities,
        selected_profile,
        selected_region,
    )


def read_config(config_file_name, aws_profile, aws_region):
    config_file = os.path.abspath(config_file_name)
    root = os.path.dirname(config_file)
    stacks = {}

    # This will raise if something goes wrong, expected
    with open(config_file, "r") as stream:
        raw_config = yaml.safe_load(stream)

    # Find all the stacks and validate them
    for name, section in raw_config.items():
        stack = parse_stack(section, root, aws_profile, aws_region)
        stacks[name] = stack

    return Config(stacks)
