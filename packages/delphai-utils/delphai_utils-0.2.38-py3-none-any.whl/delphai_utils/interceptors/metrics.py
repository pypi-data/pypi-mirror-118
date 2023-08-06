import logging
from grpc import StatusCode
from grpc.aio import ServerInterceptor, AioRpcError
from prometheus_client import Counter, Histogram, REGISTRY
from prometheus_client.registry import CollectorRegistry
from timeit import default_timer

UNARY = "UNARY"
SERVER_STREAMING = "SERVER_STREAMING"
CLIENT_STREAMING = "CLIENT_STREAMING"
BIDI_STREAMING = "BIDI_STREAMING"
UNKNOWN = "UNKNOWN"


class MetricsInterceptor(ServerInterceptor):
  registry: CollectorRegistry
  grpc_server_request_count: Counter
  grpc_server_response_count: Counter
  grpc_server_latency_seconds: Histogram

  def __init__(self, registry: CollectorRegistry = REGISTRY) -> None:
    self.registry = registry
    self.grpc_server_request_count = Counter(
      "grpc_server_request_count",
      "Total number of RPCs started on the server.",
      ["grpc_service", "grpc_method"],
      registry=registry,
    )
    self.grpc_server_response_count = Counter(
      "grpc_server_response_count",
      "Total number of RPCs completed on the server, regardless of success or failure.",
      ["grpc_type", "grpc_service", "grpc_method", "grpc_code"],
      registry=registry)
    self.grpc_server_latency_seconds = Histogram(
      "grpc_server_latency_seconds",
      "Histogram of response latency (seconds)",
      ["grpc_type", "grpc_service", "grpc_method"],
      registry=registry,
    )

  def get_method_type(self, request_streaming, response_streaming):
    """
    Infers the method type from if the request or the response is streaming.
    # The Method type is coming from:
    # https://grpc.io/grpc-java/javadoc/io/grpc/MethodDescriptor.MethodType.html
    """
    if request_streaming and response_streaming:
      return BIDI_STREAMING
    elif request_streaming and not response_streaming:
      return CLIENT_STREAMING
    elif not request_streaming and response_streaming:
      return SERVER_STREAMING
    return UNARY

  def split_method_call(self, handler_call_details):
    """
    Infers the grpc service and method name from the handler_call_details.
    """

    # e.g. /package.ServiceName/MethodName
    parts = handler_call_details.method.split("/")
    if len(parts) < 3:
      return "", "", False

    grpc_service_name, grpc_method_name = parts[1:3]
    return grpc_service_name, grpc_method_name, True

  async def intercept_service(self, continuation, handler_call_details):
    try:
      start = default_timer()
      grpc_service_name, grpc_method_name, _ = self.split_method_call(handler_call_details)
      self.grpc_server_request_count.labels(
        grpc_service=grpc_service_name,
        grpc_method=grpc_method_name,
      ).inc()
      grpc_code = None
      try:
        result = await continuation(handler_call_details)
        grpc_type = self.get_method_type(result.request_streaming, result.response_streaming)
        grpc_code = StatusCode.OK
        self.grpc_server_response_count.labels(
          grpc_type=grpc_type,
          grpc_service=grpc_service_name,
          grpc_method=grpc_method_name,
          grpc_code=grpc_code,
        ).inc()
        return result
      except AioRpcError as ex:
        grpc_code = ex.code()
        self.grpc_server_response_count.labels(
          grpc_type=grpc_type,
          grpc_service=grpc_service_name,
          grpc_method=grpc_method_name,
          grpc_code=grpc_code,
        ).inc()
        raise ex
      finally:
        elapsed = default_timer() - start
        logging.info(f'[{grpc_code}] {grpc_service_name}/{grpc_method_name} [{round(elapsed * 1000, 2)}ms]')
        self.grpc_server_latency_seconds.labels(
          grpc_type=grpc_type,
          grpc_service=grpc_service_name,
          grpc_method=grpc_method_name,
        ).observe(max(elapsed, 0))
    except Exception as ex:
      return await continuation(handler_call_details)
