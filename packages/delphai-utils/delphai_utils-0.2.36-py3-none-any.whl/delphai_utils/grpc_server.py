from typing import Union
import asyncio
import socket
from grpc import Server, aio
import grpc
from grpc_reflection.v1alpha import reflection
from grpc_health.v1 import health, health_pb2_grpc
from grpc_health.v1.health_pb2 import _HEALTH
from delphai_utils.logging import logging
from google.protobuf.descriptor import FileDescriptor
from delphai_utils.gateway import start_gateway
from delphai_utils.keycloak import update_public_keys
from jose.exceptions import JWTError
from delphai_utils.keycloak import decode_token, PublicKeyFetchError

shutdown_event = asyncio.Event()


def is_port_free(host, port):
  """
  determine whether `host` has the `port` free

  From: https://www.thepythoncode.com/article/make-port-scanner-python
  """
  s = socket.socket()
  try:
    s.connect((host, port))
  except Exception:
    return True
  else:
    return False


class NoPortFoundError(Exception):
  ...


class AuthenticationInterceptor(aio.ServerInterceptor):
  error_message: str

  def __init__(self):
    async def abort(ignored_request, context):
      await context.abort(grpc.StatusCode.UNAUTHENTICATED, self.error_message)

    self._abort = grpc.unary_unary_rpc_method_handler(abort)

  async def intercept_service(self, continuation, handler_call_details):
    metadata: aio.Metadata = handler_call_details.invocation_metadata
    authorization_header: str
    for metadatum in metadata:
      if metadatum[0] == 'authorization':
        authorization_header = metadatum[1]
    if not authorization_header:
      logging.warning('authorization header not specified')
    else:
      if 'Bearer ' not in authorization_header:
        self.error_message = 'Authorization header has the wrong format.'
        logging.error(self.error_message, authorization_header)
        return self._abort
      _, access_token = authorization_header.split('Bearer ')
      try:
        await decode_token(access_token)
      except JWTError as ex:
        self.error_message = f'Error decoding the token: {ex}'
        logging.error(self.error_message)
        return self._abort
      except PublicKeyFetchError as ex:
        self.error_message = f'Error fetching jwk from keycloak: {ex}'
        logging.error(self.error_message)
        return self._abort
    return await continuation(handler_call_details)


def find_free_port(start: int, host='127.0.0.1', num_tries=4) -> int:
  for port in range(start, start + num_tries):
    if is_port_free(host, port):
      return port
    else:
      logging.info(f'Port {port} already in use.')
  message = f'No free port found in range [{start}, {start + num_tries - 1}]'
  logging.error(message)
  raise NoPortFoundError(message)


def create_grpc_server(descriptor: FileDescriptor):
  max_length = 512 * 1024 * 1024
  server_options = [('grpc.max_send_message_length', max_length), ('grpc.max_receive_message_length', max_length)]
  server = aio.server(options=server_options, interceptors=(AuthenticationInterceptor(), ))
  server.__dict__['descriptor'] = descriptor
  health_servicer = health.HealthServicer(experimental_non_blocking=True)
  health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
  services = descriptor.services_by_name.keys()
  service_full_names = list(map(lambda service: descriptor.services_by_name[service].full_name, services))
  service_names = (
      *service_full_names,
      _HEALTH.full_name,
      reflection.SERVICE_NAME,
  )
  reflection.enable_server_reflection(service_names, server)
  return server


def start_server(server: Server,
                 gateway: bool = True,
                 grpc_port: Union[int, None] = None,
                 http_port: Union[int, None] = None):
  logging.info('starting grpc server...')
  if not grpc_port:
    grpc_port = find_free_port(8080)
  server.add_insecure_port(f'[::]:{grpc_port}')
  loop = asyncio.get_event_loop()
  loop.run_until_complete(server.start())
  logging.info(f'started grpc server on port {grpc_port}')
  try:
    if gateway:
      if not http_port:
        http_port = find_free_port(7070)
      gateway = start_gateway(server.__dict__['descriptor'], grpc_port, http_port)
      loop.create_task(gateway)
    loop.create_task(server.wait_for_termination())
    loop.create_task(update_public_keys())
    loop.run_forever()
  except KeyboardInterrupt:
    logging.info('stopped server (keyboard interrupt)')
