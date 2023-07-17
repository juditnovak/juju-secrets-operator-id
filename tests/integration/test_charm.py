#!/usr/bin/env python3
# Copyright 2023 Shayan
# See LICENSE file for licensing details.

import asyncio
import logging
from pathlib import Path
from typing import Optional

import pytest
import yaml
from pytest_operator.plugin import OpsTest

logger = logging.getLogger(__name__)

METADATA = yaml.safe_load(Path("./metadata.yaml").read_text())
APP_NAME = METADATA["name"]
UNIT0_NAME = f"{APP_NAME}/0"


@pytest.mark.abort_on_fail
async def test_build_and_deploy(ops_test: OpsTest):
    """Build the charm-under-test and deploy it together with related charms.

    Assert on the unit status before any relations/configurations take place.
    """
    # Build and deploy charm from local source folder
    charm = await ops_test.build_charm(".")
    resources = {
        "secrets-test-image": METADATA["resources"]["secrets-test-image"]["upstream-source"]
    }

    # Deploy the charm and wait for active/idle status
    await asyncio.gather(
        ops_test.model.deploy(charm, resources=resources, application_name=APP_NAME),
        ops_test.model.wait_for_idle(
            apps=[APP_NAME], status="active", raise_on_blocked=True, timeout=1000
        ),
    )


async def helper_execute_action(
    ops_test: OpsTest, action: str, params: Optional[dict[str, str]] = None
):
    if params:
        action = await ops_test.model.units.get(UNIT0_NAME).run_action(action, **params)
    else:
        action = await ops_test.model.units.get(UNIT0_NAME).run_action(action)
    action = await action.wait()
    return action.results


async def test_secret_id_label(ops_test: OpsTest):
    """Testing add_secret() return value format

    NOTE: This shouldn't work
    """
    secret_data = await helper_execute_action(ops_test, "set-secret", {"key": "key1", "value": "value1"})
    secret_labelled_data = await helper_execute_action(
            ops_test, "set-secret-labelled", {"key": "key2", "value": "value2"}
    )

    assert "//" in secret_labelled_data["secret-id"]
    assert "//" in secret_data["secret-id"]
