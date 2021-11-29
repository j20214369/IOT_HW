# IOT_HW
## Environment
```
Docker version 20.10.7
Python 3.6.9
```
## How to run
- Install project dependencies
```bash
$ sudo apt-get install protobuf-compiler
$ sudo apt-get install build-essential make
$ pip3 install -r requirements.txt
```
- Start MQTT container 
```bash
$ sudo docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
```
- Start gRPC server for fibonacci
```bash
$ cd gRPC
$ make
$ python3 server_fib.py --ip 0.0.0.0 --port 8080
```
- Open another terminal to start gRPC server for log
```bash
$ python3 gRPC/server_log.py --ip 0.0.0.0 --port 8787
```
- Open another terminal for dijango server
```bash
$ cd mysite
$ python3 manage.py migrate
$ python3 manage.py runserver 0.0.0.0:8000
```

## How to perform client request
Open a new terminal
- to see your history
```bash
$ curl http://localhost:8000/rest/logs
```
- to see the N fibonacci
```bash
$ curl -X POST http://localhost:8000/rest/fibonacci -d '{"order":N}'
```
