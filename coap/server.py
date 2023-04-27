import os
import logging

import asyncio
import aiocoap.resource as resource
import aiocoap
import requests
from decouple import config

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes


class VerySmartResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.content = b"Hello, world!"

        if config("env", "prod") == "dev":
            print("Running Env: dev")
            self.server_url = "http://localhost:8000/iot/data/"
        else:
            print("Running Env: prod")
            self.server_url = config("cloud_server", None)

    async def render_get(self, request):
        """
        This endpint does nothing. It just returns the data as it is.

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        return aiocoap.Message(payload=self.content)

    async def decrypt(self, data):
        """
        this function will TRY to decrypt the encrypted data

        Args:
            data (_type_): _description_
        """
        filename = "awesome_secret" # this is a hard coded file name.
        directory = "ssh_keys"
        path = os.path.join(directory, filename)
        if not os.path.isfile(path):
            return data

        with open(path, "rb") as key_file:
            private_key_data = key_file.read()
            loaded_private_key = serialization.load_ssh_private_key(
                private_key_data,
                password=None,
            )

        try:
            decrypted_data = loaded_private_key.decrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return decrypted_data
        except ValueError:
            return data

    async def render_post(self, request):
        """
        The magic happens here.

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        payload = request.payload
        print("-----------------------")
        print("received payload: {}".format(payload))
        
        payload = await self.decrypt(payload)
        print("decrypted payload: {}".format(payload))
        print("-----------------------")
        
        payload = payload.decode().split(" ")
        
        if len(payload) == 7:
            new_payload = {
                "acc": payload[:3],
                "gyro": payload[3:6],
                "heart": payload[6]
            }
            try:
                url = self.server_url
                resp = requests.post(url, json=new_payload)
                print("server: {} {}".format(resp.status_code, resp.text))
                return aiocoap.Message(payload=(resp.text).encode())
            except requests.exceptions.MissingSchema:
                return aiocoap.Message(payload=b'no server communicado! missing schema!')
            except requests.exceptions.ConnectionError:
                return aiocoap.Message(payload=b'no server communicado! connection err!')
        else:
            return aiocoap.Message(payload=b'no server communicado! not enough data!')


class WhoAmI(resource.Resource):
    async def render_get(self, request):
        text = ["Who Am I.\nUsed protocol: %s." % request.remote.scheme]

        text.append("Request came from %s." % request.remote.hostinfo)
        text.append("The server address used %s." %
                    request.remote.hostinfo_local)

        claims = list(request.remote.authenticated_claims)
        if claims:
            text.append("Authenticated claims of the client: %s." %
                        ", ".join(repr(c) for c in claims))
        else:
            text.append("No claims authenticated.")

        return aiocoap.Message(content_format=0,
                               payload="\n".join(text).encode('utf8'))

# Loggin Setup


logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.INFO)


async def main():
    # Create a site with the resource
    site = resource.Site()
    # site.add_resource(['.well-known', 'core'],
    # resource.WKCResource(site.get_resources_as_linkheader()))
    site.add_resource(('hello',), VerySmartResource())
    site.add_resource(['whoami'], WhoAmI())
    try:
        # Start the server on port 5683
        context = await aiocoap.Context.create_server_context(site, bind=("::", 5683))
        # Run forever
        print("Server is getting started... the future is here!")
        await asyncio.get_running_loop().create_future()
    except KeyboardInterrupt:
        print("Server is closing! The END!")

if __name__ == "__main__":
    asyncio.run(main())
