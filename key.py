import oci
import base64
from configparser import ConfigParser

def return_config_int(key):

    #Read config file
    config_object = ConfigParser()
    config_object.read(".config")

    #Get the config
    appinfo = config_object["DEFAULT"]

    return(appinfo[key])

# Retrieve secret
def read_secret_value(secret_client, secret_id):
    response = secret_client.get_secret_bundle(secret_id)
    base64_Secret_content = response.data.secret_bundle_content.content
    base64_secret_bytes = base64_Secret_content.encode('ascii')
    base64_message_bytes = base64.b64decode(base64_secret_bytes)
    secret_content = base64_message_bytes.decode('ascii')
    return secret_content

def return_secret(secret):

    #Read config file
    config_object = ConfigParser()
    config_object.read(".config")

    #Get the secret
    appinfo = config_object[return_config_int("env")]

    # Replace secret_id value below with the ocid of your secret
    secret_id = appinfo[secret]

    # By default this will hit the auth service in the region the instance is running.
    signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()

    # In the base case, configuration does not need to be provided as the region and tenancy are obtained from the InstancePrincipalsSecurityTokenSigner
    #identity_client = oci.identity.IdentityClient(config={}, signer=signer)

    # Get instance principal context
    secret_client = oci.secrets.SecretsClient(config={}, signer=signer)

    # Get secret contents
    secret_contents = read_secret_value(secret_client, secret_id)

    return (secret_contents)

def return_config(key):

    #Read config file
    config_object = ConfigParser()
    config_object.read(".config")

    #Get the config
    appinfo = config_object[return_config_int("env")]

    return(appinfo[key])
