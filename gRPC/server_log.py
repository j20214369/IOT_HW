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
