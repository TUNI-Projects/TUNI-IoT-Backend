import asyncio
import aiocoap
from decouple import config
import sys

COAP_SERVER_ADDRESS = config('coap_server_address', None)
COAP_PORT = config('coap_port', None)


async def get():
    # Create a context and a request
    print("-----------------------------------------")
    print("Testing GET request Endpoints")
    print("-----------------------------------------")
    context = await aiocoap.Context.create_client_context()
    request = aiocoap.Message(code=aiocoap.GET)

    # Set the request URI to the hello resource we created
    request.set_request_uri(
        'coap://{}:{}/hello'.format(COAP_SERVER_ADDRESS, COAP_PORT))

    # Send the request and wait for the response
    response = await context.request(request).response

    # Print the response payload
    print("Response >> ", response.payload.decode())
    print("-----------------------------------------")

    request.set_request_uri(
        'coap://{}:{}/whoami'.format(COAP_SERVER_ADDRESS, COAP_PORT))

    # Send the request and wait for the response
    response = await context.request(request).response

    # Print the response payload
    print("Response: >> ")
    print(response.payload.decode())


async def post():
    print("-----------------------------------------")
    print("Testing Post Request End Points")
    print("-----------------------------------------")
    # Create a context and a request
    context = await aiocoap.Context.create_client_context()
    request = aiocoap.Message(code=aiocoap.POST)

    # Set the request URI to the hello resource we created
    request.set_request_uri(
        'coap://{}:{}/hello'.format(COAP_SERVER_ADDRESS, COAP_PORT))

    # Set the request payload
    payload = b"Hello, server! Your Payload goes here in bytes"
    request.payload = payload
    print("Payload to server: {}".format(payload))
    print("Payload type: ", type(payload))

    # Send the request and wait for the response
    response = await context.request(request).response

    # Print the response payload
    print("From Server: ", response.payload.decode())

if __name__ == "__main__":
    if COAP_SERVER_ADDRESS is None or COAP_PORT is None:
        sys.exit("COAP Server Address or Port Not Found. Terminated!")
    choice = input(
        "choose 1 to test get request, choose 2 to test post request >> ")
    if choice == "1":
        asyncio.run(get())
    elif choice == "2":
        asyncio.run(post())
    else:
        print("choice is either 1 or 2.")
