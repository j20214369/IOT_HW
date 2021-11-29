
import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse

import grpc
from concurrent import futures
import log_pb2
import log_pb2_grpc

import paho.mqtt.client as mqtt

import threading

mqtt_host = "localhost"
mqtt_port = 1883

history = list()

def on_message(client, obj, msg):
    history.append(int(msg.payload))
    print(f"Get value:{int(msg.payload)}")
    print(f"History:{history}")

def main():
    # Establish connection to mqtt broker
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(host = mqtt_host, port = mqtt_port)
    client.subscribe('log', 0)

    try:
        client.loop_forever()
    except KeyboardInterrupt as e:
        pass



class LogCalculatorServicer(log_pb2_grpc.LogCalculatorServicer):

    def __init__(self):
        pass

    def Compute(self, request, context):
        response = log_pb2.LogResponse()
        for i in history:
            response.log.append(i)
        return response



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", type=str)
    parser.add_argument("--port", default=8080, type=int)
    args = vars(parser.parse_args())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = LogCalculatorServicer()
    log_pb2_grpc.add_LogCalculatorServicer_to_server(servicer, server)
    t = threading.Thread(target = main)
    try:
        server.add_insecure_port(f"{args['ip']}:{args['port']}")
        t.start()
        server.start()
        print(f"Run log gRPC Server at {args['ip']}:{args['port']}")
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass                                                                                                                                
