from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TripRequest(_message.Message):
    __slots__ = ("userId",)
    USERID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    def __init__(self, userId: _Optional[str] = ...) -> None: ...

class CreateTripRequest(_message.Message):
    __slots__ = ("accountId", "entry", "exit")
    ACCOUNTID_FIELD_NUMBER: _ClassVar[int]
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    EXIT_FIELD_NUMBER: _ClassVar[int]
    accountId: str
    entry: str
    exit: str
    def __init__(self, accountId: _Optional[str] = ..., entry: _Optional[str] = ..., exit: _Optional[str] = ...) -> None: ...

class UpdateTripRequest(_message.Message):
    __slots__ = ("tripId", "entry", "exit")
    TRIPID_FIELD_NUMBER: _ClassVar[int]
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    EXIT_FIELD_NUMBER: _ClassVar[int]
    tripId: str
    entry: str
    exit: str
    def __init__(self, tripId: _Optional[str] = ..., entry: _Optional[str] = ..., exit: _Optional[str] = ...) -> None: ...

class TripResponse(_message.Message):
    __slots__ = ("tripId", "accountId", "entry", "exit", "timestamp")
    TRIPID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNTID_FIELD_NUMBER: _ClassVar[int]
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    EXIT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    tripId: str
    accountId: str
    entry: str
    exit: str
    timestamp: str
    def __init__(self, tripId: _Optional[str] = ..., accountId: _Optional[str] = ..., entry: _Optional[str] = ..., exit: _Optional[str] = ..., timestamp: _Optional[str] = ...) -> None: ...

class TripList(_message.Message):
    __slots__ = ("trips",)
    TRIPS_FIELD_NUMBER: _ClassVar[int]
    trips: _containers.RepeatedCompositeFieldContainer[TripResponse]
    def __init__(self, trips: _Optional[_Iterable[_Union[TripResponse, _Mapping]]] = ...) -> None: ...

class DeleteResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
