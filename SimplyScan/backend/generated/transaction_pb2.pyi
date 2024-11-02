from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TransactionRequest(_message.Message):
    __slots__ = ("userId",)
    USERID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    def __init__(self, userId: _Optional[str] = ...) -> None: ...

class CreateTransactionRequest(_message.Message):
    __slots__ = ("amount", "accountId")
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    ACCOUNTID_FIELD_NUMBER: _ClassVar[int]
    amount: float
    accountId: str
    def __init__(self, amount: _Optional[float] = ..., accountId: _Optional[str] = ...) -> None: ...

class UpdateTransactionRequest(_message.Message):
    __slots__ = ("transactionId", "amount")
    TRANSACTIONID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    transactionId: str
    amount: float
    def __init__(self, transactionId: _Optional[str] = ..., amount: _Optional[float] = ...) -> None: ...

class TransactionResponse(_message.Message):
    __slots__ = ("transactionId", "amount", "accountId", "timestamp")
    TRANSACTIONID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    ACCOUNTID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    transactionId: str
    amount: float
    accountId: str
    timestamp: str
    def __init__(self, transactionId: _Optional[str] = ..., amount: _Optional[float] = ..., accountId: _Optional[str] = ..., timestamp: _Optional[str] = ...) -> None: ...

class TransactionList(_message.Message):
    __slots__ = ("transactions",)
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    transactions: _containers.RepeatedCompositeFieldContainer[TransactionResponse]
    def __init__(self, transactions: _Optional[_Iterable[_Union[TransactionResponse, _Mapping]]] = ...) -> None: ...

class DeleteResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
