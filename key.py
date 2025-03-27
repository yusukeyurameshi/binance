#!/usr/bin/python3

import oci
import base64
from configparser import ConfigParser

class ConfigManager:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read(".config")
        self.env = self._get_env()

    def _get_env(self):
        """Retorna o ambiente atual (dev, prod, etc)"""
        return self.config["DEFAULT"]["env"]

    def get_config(self, key):
        """Retorna uma configuração do arquivo .config"""
        return self.config[self.env][key]

    def get_config_int(self, key):
        """Retorna uma configuração inteira do arquivo .config"""
        return int(self.config["DEFAULT"][key])

class SecretManager:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.secret_client = self._initialize_secret_client()

    def _initialize_secret_client(self):
        """Inicializa o cliente de segredos da OCI"""
        signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
        return oci.secrets.SecretsClient(config={}, signer=signer)

    def _read_secret_value(self, secret_id):
        """Lê o valor de um segredo da OCI"""
        response = self.secret_client.get_secret_bundle(secret_id)
        base64_Secret_content = response.data.secret_bundle_content.content
        base64_secret_bytes = base64_Secret_content.encode('ascii')
        base64_message_bytes = base64.b64decode(base64_secret_bytes)
        return base64_message_bytes.decode('ascii')

    def get_secret(self, secret):
        """Retorna um segredo da OCI"""
        secret_id = self.config_manager.get_config(secret)
        return self._read_secret_value(secret_id)

class KeyManager:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.secret_manager = SecretManager()

    def return_config(self, key):
        """Interface para retornar configurações"""
        return self.config_manager.get_config(key)

    def return_secret(self, secret):
        """Interface para retornar segredos"""
        return self.secret_manager.get_secret(secret)

    def return_config_int(self, key):
        """Interface para retornar configurações inteiras"""
        return self.config_manager.get_config_int(key)

# Instância global para manter compatibilidade com o código existente
key_manager = KeyManager()

# Funções de interface para manter compatibilidade com o código existente
def return_config(key):
    return key_manager.return_config(key)

def return_secret(secret):
    return key_manager.return_secret(secret)

def return_config_int(key):
    return key_manager.return_config_int(key)
