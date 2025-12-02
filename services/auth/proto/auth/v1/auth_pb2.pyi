from common.v1 import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoginRequest(_message.Message):
    __slots__ = ("email", "password")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class LoginResponse(_message.Message):
    __slots__ = ("success", "user_id", "token")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    success: bool
    user_id: _common_pb2.Uuid
    token: str
    def __init__(self, success: bool = ..., user_id: _Optional[_Union[_common_pb2.Uuid, _Mapping]] = ..., token: _Optional[str] = ...) -> None: ...

class RegisterRequest(_message.Message):
    __slots__ = ("name", "email", "password")
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    name: str
    email: str
    password: str
    def __init__(self, name: _Optional[str] = ..., email: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class RegisterResponse(_message.Message):
    __slots__ = ("success", "error", "time")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: str
    time: int
    def __init__(self, success: bool = ..., error: _Optional[str] = ..., time: _Optional[int] = ...) -> None: ...

class ResendOtpRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class ResendOtpResponse(_message.Message):
    __slots__ = ("success", "time")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    success: bool
    time: int
    def __init__(self, success: bool = ..., time: _Optional[int] = ...) -> None: ...

class VerifyOtpRequest(_message.Message):
    __slots__ = ("email", "otp")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    OTP_FIELD_NUMBER: _ClassVar[int]
    email: str
    otp: str
    def __init__(self, email: _Optional[str] = ..., otp: _Optional[str] = ...) -> None: ...

class VerifyOtpResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
