# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: trip.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'trip.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ntrip.proto\x12\x04trip\"\x1d\n\x0bTripRequest\x12\x0e\n\x06userId\x18\x01 \x01(\t\"C\n\x11\x43reateTripRequest\x12\x11\n\taccountId\x18\x01 \x01(\t\x12\r\n\x05\x65ntry\x18\x02 \x01(\t\x12\x0c\n\x04\x65xit\x18\x03 \x01(\t\"@\n\x11UpdateTripRequest\x12\x0e\n\x06tripId\x18\x01 \x01(\t\x12\r\n\x05\x65ntry\x18\x02 \x01(\t\x12\x0c\n\x04\x65xit\x18\x03 \x01(\t\"a\n\x0cTripResponse\x12\x0e\n\x06tripId\x18\x01 \x01(\t\x12\x11\n\taccountId\x18\x02 \x01(\t\x12\r\n\x05\x65ntry\x18\x03 \x01(\t\x12\x0c\n\x04\x65xit\x18\x04 \x01(\t\x12\x11\n\ttimestamp\x18\x05 \x01(\t\"-\n\x08TripList\x12!\n\x05trips\x18\x01 \x03(\x0b\x32\x12.trip.TripResponse\"\x10\n\x0e\x44\x65leteResponse2\xab\x02\n\x04Trip\x12.\n\x07GetTrip\x12\x11.trip.TripRequest\x1a\x0e.trip.TripList\"\x00\x12:\n\x0fGetTripByUserId\x12\x11.trip.TripRequest\x1a\x12.trip.TripResponse\"\x00\x12;\n\nUpdateTrip\x12\x17.trip.UpdateTripRequest\x1a\x12.trip.TripResponse\"\x00\x12;\n\nCreateTrip\x12\x17.trip.CreateTripRequest\x1a\x12.trip.TripResponse\"\x00\x12=\n\nDeleteTrip\x12\x17.trip.UpdateTripRequest\x1a\x14.trip.DeleteResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'trip_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TRIPREQUEST']._serialized_start=20
  _globals['_TRIPREQUEST']._serialized_end=49
  _globals['_CREATETRIPREQUEST']._serialized_start=51
  _globals['_CREATETRIPREQUEST']._serialized_end=118
  _globals['_UPDATETRIPREQUEST']._serialized_start=120
  _globals['_UPDATETRIPREQUEST']._serialized_end=184
  _globals['_TRIPRESPONSE']._serialized_start=186
  _globals['_TRIPRESPONSE']._serialized_end=283
  _globals['_TRIPLIST']._serialized_start=285
  _globals['_TRIPLIST']._serialized_end=330
  _globals['_DELETERESPONSE']._serialized_start=332
  _globals['_DELETERESPONSE']._serialized_end=348
  _globals['_TRIP']._serialized_start=351
  _globals['_TRIP']._serialized_end=650
# @@protoc_insertion_point(module_scope)