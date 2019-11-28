#!/usr/bin/env python
import os
from typing import Dict, Type
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.keyvault.models import (
    Permissions,
    Sku,
    AccessPolicyEntry,
    VaultProperties,
    VaultCreateOrUpdateParameters
)
from aci_tasks.cloud.util import _get_credentials, _poll_for_complete


class AciKeyVaultSecretStore(dict):
    def __setitem__(self, key, item):
        _add_item_to_key_vault(key, item)

    def __getitem__(self, key):
        return _get_item_from_key_vault(key)

    def __repr__(self):
        return "KeyVaultStore()"

    def __delitem__(self, key):
        _remove_item_from_key_vault(key)

    def __len__(self):
        return len(self.items())

    def __contains__(self, item):
        return item in self.items()

    def __iter__(self):
        return iter(self.items())

    def items(self):
        result = _get_all_items_from_key_vault()
        return result.items()


class AciKeyVaultManager():
    def __init__(self, config):
        self.config = config

    def create(self):
        secret_permissions = ['all']

        permissions = Permissions(secrets=secret_permissions)

        access_policy = AccessPolicyEntry(
            tenant_id=self.config.tenant_id,
            object_id=self.config.client_object_id,
            permissions=permissions
        )

        sku = Sku(name="standard")

        properties = VaultProperties(
            tenant_id=self.config.tenant_id,
            sku=sku,
            access_policies=[access_policy]
        )

        vault_paramerters = VaultCreateOrUpdateParameters(
            location="eastus",
            properties=properties
        )

        client = self._get_kv_client()
        result = client.vaults.create_or_update(
            resource_group_name=self.config.resource_group_name,
            vault_name=self.config.key_vault_name,
            parameters=vault_paramerters
        )
        _poll_for_complete(result)

    def _get_kv_client(self):
        return KeyVaultManagementClient(
            _get_credentials(self.config), self.config.subscription_id
        )


def _get_client() -> Type[SecretClient]:
    key_vault_url = os.getenv("KEYVAULTURL")
    if key_vault_url is None:
        raise ValueError("Need to set env var: KEYVAULTURL=https://my-key-vault.vault.azure.net/")

    credential = DefaultAzureCredential()
    return SecretClient(vault_url=key_vault_url, credential=credential)


def _add_item_to_key_vault(key, item):
    client = _get_client()
    if "_" in key:
        raise ValueError("Key cannot contain underscores.")

    client.set_secret(key, item)


def _remove_item_from_key_vault(key):
    client = _get_client()
    client.begin_delete_secret(key).result()


def _get_item_from_key_vault(key):
    client = _get_client()
    return client.get_secret(key).value


def _get_all_items_from_key_vault() -> Dict:
    secrets = {}
    client = _get_client()
    result = client.list_properties_of_secrets()

    for sec in result:
        secrets[sec.name] = client.get_secret(sec.name).value

    return secrets
