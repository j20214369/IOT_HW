from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

import json

import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "../../gRPC-with-protobuf/build/service/")
sys.path.insert(0, BUILD_DIR)

import grpc
import fib_pb2
import fib_pb2_grpc
import log_pb2
import log_pb2_grpc


import paho.mqtt.client as mqtt

fibserver = "0.0.0.0:8080"
logserver = "0.0.0.0:8787"
mqtt_host = "localhost"
mqtt_port = 1883

# Create your views here.
class FibView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        text = request.body.decode('utf-8')
        body = json.loads(text)
        order = body['order']


        # Establish connection to mqtt broker
        client = mqtt.Client()
        client.connect(host = mqtt_host, port = mqtt_port)
        client.loop_start()
        payload = order
        client.publish(topic = 'log', payload = payload)
        client.loop_stop()


        host = fibserver
        with grpc.insecure_channel(host) as channel:
            stub = fib_pb2_grpc.FibCalculatorStub(channel)

            request = fib_pb2.FibRequest()
            request.order = order

            response = stub.Compute(request)
            

        return Response(data={ response.value }, status=200)

class LogView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        host = logserver
        with grpc.insecure_channel(host) as channel:
            stub = log_pb2_grpc.LogCalculatorStub(channel)

            request = log_pb2.LogRequest()

            response = stub.Compute(request)

        return Response(data={ 'history': response.log[:] }, status=200)

