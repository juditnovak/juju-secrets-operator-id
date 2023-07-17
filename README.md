<!--
Avoid using this README file for information that is maintained or published elsewhere, e.g.:

* metadata.yaml > published on Charmhub
* documentation > published on (or linked to from) Charmhub
* detailed contribution guide > documentation or CONTRIBUTING.md

Use links instead.
-->

# secrets-test ID

Small demonstration of the unexpected beahvior observed regarding secret IDs

Initially they had the shape of

    - `secret:<secret ID>`

However as --demonstrated here-- in Juju 3.1 now they appear as

    - `secret://<model UUID >/<secret ID>

## Issue

Demonstration of the issue is visible in the correpsonding [Integration Test](tests/integration/test_charm.py) -- run successfully by the corresponding pipeline.

```
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
```
