import asyncio
import aiocoap

async def get():
    # Create a context and a request
    print("-----------------------------------------")
    print("Testing GET request Endpoints")
    print("-----------------------------------------")
    context = await aiocoap.Context.create_client_context()
    request = aiocoap.Message(code=aiocoap.GET)

    # Set the request URI to the hello resource we created
    request.set_request_uri('coap://localhost:5683/hello')

    # Send the request and wait for the response
    response = await context.request(request).response

    # Print the response payload
    print("Response >> ", response.payload.decode())
    print("-----------------------------------------")
    
    request.set_request_uri('coap://localhost:5683/whoami')
    
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
    request.set_request_uri('coap://localhost/hello')

    # Set the request payload
    payload = b"Hello, server!"
    request.payload = payload
    print("Payload to server: {}".format(payload))
    print("Payload type: ", type(payload))

    # Send the request and wait for the response
    response = await context.request(request).response

    # Print the response payload
    print(response.payload.decode())

if __name__ == "__main__":
    choice = input("choose 1 to test get request, choose 2 to test post request >> ")
    if choice == "1":
        asyncio.run(get())
    elif choice == "2":
        asyncio.run(post())
    else:
        print("choice is either 1 or 2.")