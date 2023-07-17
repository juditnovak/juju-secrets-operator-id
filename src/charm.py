#!/usr/bin/env python3
# Copyright 2023 Shayan
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

https://discourse.charmhub.io/t/4208
"""

import logging

import ops
from ops import ActiveStatus
from ops.charm import ActionEvent

# Log messages can be retrieved using juju debug-log
logger = logging.getLogger(__name__)

VALID_LOG_LEVELS = ["info", "debug", "warning", "error", "critical"]
PEER = "charm-peer"


class SecretsTestCharm(ops.CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)

        self.framework.observe(self.on.start, self._on_start)

        self.framework.observe(self.on.set_secret_action, self._on_set_secret_action)
        self.framework.observe(self.on.set_secret_labelled_action, self._on_set_secret_labelled)

    def _on_start(self, event) -> None:
        self.unit.status = ActiveStatus()

    def _on_set_secret_action(self, event: ActionEvent):
        key, value = event.params.get("key"), event.params.get("value")
        event.set_results({"secret-id": self.set_secret(key, value)})

    def _on_set_secret_labelled(self, event: ActionEvent):
        key, value = event.params.get("key"), event.params.get("value")
        event.set_results({"secret-id": self.set_secret_labelled(key, value)})

    @property
    def peers(self) -> ops.model.Relation:
        """Retrieve the peer relation (`ops.model.Relation`)."""
        return self.model.get_relation(PEER)

    @property
    def app_peer_data(self) -> dict[str, str]:
        """Application peer relation data object."""
        if self.peers is None:
            return {}

        return self.peers.data[self.app]

    def set_secret(self, key: str, value: str) -> None:
        """Set the secret in the juju secret storage."""
        content = {
            key: value,
        }
        secret = self.app.add_secret(content)
        self.app_peer_data["secret-id"] = secret.id
        logger.info(f"Added secret {secret.id} to {content}")

        return secret.id

    def set_secret_labelled(self, key: str, value: str) -> None:
        """Set the secret in the juju secret storage."""
        content = {
            key: value,
        }
        secret = self.app.add_secret(content, label=f"secret-{key}")
        self.app_peer_data["secret-id"] = secret.id
        logger.info(f"Added secret {secret.id} to {content}")

        return secret.id


if __name__ == "__main__":  # pragma: nocover
    ops.main(SecretsTestCharm)
