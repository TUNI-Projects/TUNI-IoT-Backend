import os
import asyncio
import aiocoap
from decouple import config
import sys
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_ssh_public_key

if config("env", "prod") == "dev":
    print("Running Env: dev")
    COAP_SERVER_ADDRESS = "localhost"
    COAP_PORT = 5683
else:
    print("Running Env: prod")
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


async def encrypt(data: bytes):
    """encrypt the data using public key encryption system.
    if there's no public key available, it will send the data as it is.

    Args:
        data (bytes): _description_
    """
    filename = "awesome_secret.pub"
    directory = "ssh_keys"
    path = os.path.join(directory, filename)
    if not os.path.isfile(path):
        return data
    else:
        with open(os.path.join(directory, filename), "rb") as key_file:
            ssh_key_data = key_file.read()
            loaded_public_key = load_ssh_public_key(ssh_key_data)

        encrypted_data = loaded_public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_data


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
    payload = b"0.05 -0.99 -0.02 -0.39 0.33 -0.16 109"
    print("Payload to server: {}".format(payload))
    payload = await encrypt(payload)
    print("Encrypted payload to server: {}".format(payload))
    request.payload = payload
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
