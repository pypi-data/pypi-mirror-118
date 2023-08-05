import logging
import socket
from ssl import SSLContext
from typing import Union, Tuple

from httpcore import SyncConnectionPool
from httpcore._backends.sync import SyncBackend, SyncSocketStream
from httpcore._sync.connection import SyncHTTPConnection
from httpx import HTTPTransport, create_ssl_context, Limits
from httpx._config import DEFAULT_LIMITS
from httpx._types import VerifyTypes, CertTypes

from tcp_tls_tunnel.dto import AdapterOptions, ProxyOptions, TunnelOptions
from tcp_tls_tunnel.requests_adapter import create_tunnel_connection

logging.basicConfig(level=logging.WARNING)


class TunnelHTTPTransport(HTTPTransport):
    def __init__(
            self,
            adapter_opts: AdapterOptions,
            proxy_opts: ProxyOptions = None,
            verify: VerifyTypes = True,
            cert: CertTypes = None,
            http1: bool = True,
            limits: Limits = DEFAULT_LIMITS,
            trust_env: bool = True,
            retries: int = 0,
            backend: str = "sync",
    ) -> None:
        super(TunnelHTTPTransport, self).__init__()
        ssl_context = create_ssl_context(verify=verify, cert=cert, trust_env=trust_env)

        self._pool = TunnelHTTP20SyncConnectionPool(
            adapter_opts=adapter_opts,
            proxy_opts=proxy_opts,
            ssl_context=ssl_context,
            http1=http1,
            http2=True,
            retries=retries,
            max_connections=limits.max_connections,
            max_keepalive_connections=limits.max_keepalive_connections,
            keepalive_expiry=limits.keepalive_expiry,
            backend=backend
        )


class TunnelSyncSocketStream(SyncSocketStream):

    def __init__(self, sock: socket.socket, proto: str):
        super(TunnelSyncSocketStream, self).__init__(sock=sock)
        self.proto = proto

    def get_http_version(self) -> str:
        return "HTTP/2" if self.proto == "h2" else "HTTP/1.1"


class TunnelHTTP20SyncConnectionPool(SyncConnectionPool):

    def __init__(
            self,
            adapter_opts: AdapterOptions,
            proxy_opts: ProxyOptions,
            ssl_context: SSLContext = None,
            max_connections: int = None,
            max_keepalive_connections: int = None,
            keepalive_expiry: float = None,
            http1: bool = True,
            http2: bool = False,
            uds: str = None,
            local_address: str = None,
            retries: int = 0,
            max_keepalive: int = None,
            backend: Union[SyncBackend, str] = "sync",
    ):
        super(TunnelHTTP20SyncConnectionPool, self).__init__(
            ssl_context=ssl_context,
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive_connections,
            keepalive_expiry=keepalive_expiry,
            http1=http1,
            http2=http2,
            uds=uds,
            local_address=local_address,
            retries=retries,
            max_keepalive=max_keepalive,
            backend=backend
        )
        self.adapter_opts = adapter_opts
        self.proxy_opts = proxy_opts

    def _create_connection(
        self,
        origin: Tuple[bytes, bytes, int],
    ) -> SyncHTTPConnection:
        host, port = origin[1].decode("utf-8"), origin[2]
        secure = int("https" == origin[0].decode("utf-8"))

        conn, proto = create_tunnel_connection(
            tunnel_opts=TunnelOptions(
                host=self.adapter_opts.host,
                port=self.adapter_opts.port,
                auth_login=self.adapter_opts.auth_login,
                auth_password=self.adapter_opts.auth_password,
                client=self.adapter_opts.client,
                secure=True if secure == 1 else False,
                http2=True
            ),
            dest_host=host,
            dest_port=port,
            proxy=self.proxy_opts,
            server_name=None  # TODO: server_name
        )

        return SyncHTTPConnection(
            origin=origin,
            http1=self._http1,
            http2=self._http2,
            keepalive_expiry=self._keepalive_expiry,
            uds=self._uds,
            ssl_context=self._ssl_context,
            local_address=self._local_address,
            socket=TunnelSyncSocketStream(sock=conn.sock, proto=proto),
            retries=self._retries,
            backend=self._backend,
        )
