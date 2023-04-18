import logging

import asyncio
import aiocoap.resource as resource
import aiocoap
import requests
from decouple import config


class VerySmartResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.content = b"Hello, world!"

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    async def render_post(self, request):
        payload = request.payload
        print("received payload: {}".format(payload))
        payload = payload.decode().split(" ")

        if len(payload) == 6:
            new_payload = {
                "acc": payload[:3],
                "gyro": payload[3:6],
                "heart": payload[6]
            }
            try:
                url = config("cloud_server", None)
                resp = requests.post(url, json=new_payload)
                print("server: {}-{}".format(resp.status_code, resp.text))
                return aiocoap.Message(payload=(resp.text).encode())
            except requests.exceptions.MissingSchema:
                return aiocoap.Message(payload=b'no server communicado!')
        else:
            return aiocoap.Message(payload=b'no server communicado!')


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
