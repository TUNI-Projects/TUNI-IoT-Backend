# Very Smart Backend - CoAP Server

This is the coap server instances for very smart backend. `.well-known/core` endpoint does not work at the point of this writing. There is a `test_client.py` file, it can be used to test the available endpoints.

## How to

1. `pip install -r requirements.txt` to install all the required packages in the virtualenv.
2. `python3 server.py` to run the server or `nohup python3 server.py &` to run in detach mode.
3. `python3 test_client.py` to test the server's endpoints. Other than testing the endpoints availability, it has no other practical function. 

### Endpoints

IP_ADDRESS = 172.105.117.206
PORT = 5683

1. Get - [coap://(IP_ADDRESS):(PORT)/hello] - Simple Hello World Endpoint.
2. Get - [coap://(IP_ADDRESS):(PORT)/whoami] - Returns Who Am I Response.
3. Post - [coap://(IP_ADDRESS):(PORT)/hello] - General purpose Post Endpoint, for now.

### Contributor

1. Mohammad Asif Ibtehaz
2. Jesper Vuoristo
3. Rukayat Mumuney
4. Yuhang Du
