# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import biderection_pb2 as biderection__pb2

GRPC_GENERATED_VERSION = '1.68.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in biderection_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class BidirectionalStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetServerResponse = channel.stream_stream(
                '/bidirection.Bidirectional/GetServerResponse',
                request_serializer=biderection__pb2.Message.SerializeToString,
                response_deserializer=biderection__pb2.Message.FromString,
                _registered_method=True)


class BidirectionalServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetServerResponse(self, request_iterator, context):
        """A Bidirectional Streaming RPC

        Accepts a stream of requests, and route is traversed
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BidirectionalServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetServerResponse': grpc.stream_stream_rpc_method_handler(
                    servicer.GetServerResponse,
                    request_deserializer=biderection__pb2.Message.FromString,
                    response_serializer=biderection__pb2.Message.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'bidirection.Bidirectional', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('bidirection.Bidirectional', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Bidirectional(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetServerResponse(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            '/bidirection.Bidirectional/GetServerResponse',
            biderection__pb2.Message.SerializeToString,
            biderection__pb2.Message.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
