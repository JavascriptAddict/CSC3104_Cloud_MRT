# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: transaction.proto
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
    'transaction.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11transaction.proto\x12\x0btransaction\"$\n\x12TransactionRequest\x12\x0e\n\x06userId\x18\x01 \x01(\t\"=\n\x18\x43reateTransactionRequest\x12\x0e\n\x06\x61mount\x18\x01 \x01(\x02\x12\x11\n\taccountId\x18\x02 \x01(\t\"A\n\x18UpdateTransactionRequest\x12\x15\n\rtransactionId\x18\x01 \x01(\t\x12\x0e\n\x06\x61mount\x18\x02 \x01(\x02\"b\n\x13TransactionResponse\x12\x15\n\rtransactionId\x18\x01 \x01(\t\x12\x0e\n\x06\x61mount\x18\x02 \x01(\x02\x12\x11\n\taccountId\x18\x03 \x01(\t\x12\x11\n\ttimestamp\x18\x04 \x01(\t\"I\n\x0fTransactionList\x12\x36\n\x0ctransactions\x18\x01 \x03(\x0b\x32 .transaction.TransactionResponse\"\x10\n\x0e\x44\x65leteResponse2\xfb\x02\n\x0bTransaction\x12Q\n\x0eGetTransaction\x12\x1f.transaction.TransactionRequest\x1a\x1c.transaction.TransactionList\"\x00\x12^\n\x11UpdateTransaction\x12%.transaction.UpdateTransactionRequest\x1a .transaction.TransactionResponse\"\x00\x12^\n\x11\x43reateTransaction\x12%.transaction.CreateTransactionRequest\x1a .transaction.TransactionResponse\"\x00\x12Y\n\x11\x44\x65leteTransaction\x12%.transaction.UpdateTransactionRequest\x1a\x1b.transaction.DeleteResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transaction_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TRANSACTIONREQUEST']._serialized_start=34
  _globals['_TRANSACTIONREQUEST']._serialized_end=70
  _globals['_CREATETRANSACTIONREQUEST']._serialized_start=72
  _globals['_CREATETRANSACTIONREQUEST']._serialized_end=133
  _globals['_UPDATETRANSACTIONREQUEST']._serialized_start=135
  _globals['_UPDATETRANSACTIONREQUEST']._serialized_end=200
  _globals['_TRANSACTIONRESPONSE']._serialized_start=202
  _globals['_TRANSACTIONRESPONSE']._serialized_end=300
  _globals['_TRANSACTIONLIST']._serialized_start=302
  _globals['_TRANSACTIONLIST']._serialized_end=375
  _globals['_DELETERESPONSE']._serialized_start=377
  _globals['_DELETERESPONSE']._serialized_end=393
  _globals['_TRANSACTION']._serialized_start=396
  _globals['_TRANSACTION']._serialized_end=775
# @@protoc_insertion_point(module_scope)
