from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AccountRequest(_message.Message):
    __slots__ = ("userId",)
    USERID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    def __init__(self, userId: _Optional[str] = ...) -> None: ...

class CreateAccountRequest(_message.Message):
    __slots__ = ("name", "nric", "username", "password")
    NAME_FIELD_NUMBER: _ClassVar[int]
    NRIC_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    name: str
    nric: str
    username: str
    password: str
    def __init__(self, name: _Optional[str] = ..., nric: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class UpdateAccountRequest(_message.Message):
    __slots__ = ("userId", "name", "nric", "username", "password", "accountStatus")
    USERID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NRIC_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    ACCOUNTSTATUS_FIELD_NUMBER: _ClassVar[int]
    userId: str
    name: str
    nric: str
    username: str
    password: str
    accountStatus: str
    def __init__(self, userId: _Optional[str] = ..., name: _Optional[str] = ..., nric: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., accountStatus: _Optional[str] = ...) -> None: ...

class AccountResponse(_message.Message):
    __slots__ = ("userId", "name", "nric", "username", "password", "accountStatus", "walletId")
    USERID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NRIC_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    ACCOUNTSTATUS_FIELD_NUMBER: _ClassVar[int]
    WALLETID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    name: str
    nric: str
    username: str
    password: str
    accountStatus: str
    walletId: str
    def __init__(self, userId: _Optional[str] = ..., name: _Optional[str] = ..., nric: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., accountStatus: _Optional[str] = ..., walletId: _Optional[str] = ...) -> None: ...

class DeleteResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: int
    message: str
    def __init__(self, status: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...