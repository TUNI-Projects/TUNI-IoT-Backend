# Very Smart Backend

Very Smart Backend is the intended backend for IoT Project. The Project is separated into two parts, CoapServer which is in `coap` directory and main `django` backend. We have used `sqlit3` database to manage the data, because we simply didn't want to take the pain to create a postgresql database. Check `coap` directory `readme` to run the `coap` server.

## How to

1. `pip install -r requirements.txt` to install all the required packages in the virtualenv.
2. `python3 manage.py runserver` to run the server.

## API

1. Fetch (Heart/Gyro/Acc Records)
    * Request Type: Get
    * URL: [http://172.105.117.206:9889/api/records/]
    * URL Parameters:
        * choice=heart/acc/gyro.
        * start_date=start_date in seconds.
        * end_date=end_date in seconds.

2. Fetch (Current Data) [Socket Connection]

### Contributor

1. Mohammad Asif Ibtehaz
2. Jesper Vuoristo
3. Rukayat Mumuney
4. Yuhang Du
