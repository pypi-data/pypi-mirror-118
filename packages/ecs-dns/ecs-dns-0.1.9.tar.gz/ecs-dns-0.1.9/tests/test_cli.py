#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ecs_dns` package."""

import pytest
from click.testing import CliRunner

from ecs_dns import _cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()

    # test no args
    result = runner.invoke(_cli.cli)
    assert result.exit_code == 2
    assert "Error: Missing argument 'DNS_NAME'" in result.output

    # test help command
    help_result = runner.invoke(_cli.cli, ["--help"])
    assert help_result.exit_code == 0
    expected_args = [
        "-c, --container-name TEXT",
        "Container name to create a record for.",
        "-p, --port INTEGER",
        "Port for the healthcheck to query.",
        "--protocol TEXT",
        "Protocol for the healthcheck to use.",
        "--help",
        "Show this message and exit.",
    ]
    assert all(arg in help_result.output for arg in expected_args)
