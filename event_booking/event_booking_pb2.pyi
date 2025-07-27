from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Event(_message.Message):
    __slots__ = ("id", "name", "total_tickets", "booked_tickets")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TOTAL_TICKETS_FIELD_NUMBER: _ClassVar[int]
    BOOKED_TICKETS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    total_tickets: int
    booked_tickets: int
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., total_tickets: _Optional[int] = ..., booked_tickets: _Optional[int] = ...) -> None: ...

class CreateEventRequest(_message.Message):
    __slots__ = ("name", "total_tickets")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TOTAL_TICKETS_FIELD_NUMBER: _ClassVar[int]
    name: str
    total_tickets: int
    def __init__(self, name: _Optional[str] = ..., total_tickets: _Optional[int] = ...) -> None: ...

class BookEventRequest(_message.Message):
    __slots__ = ("event_id", "num_tickets")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    NUM_TICKETS_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    num_tickets: int
    def __init__(self, event_id: _Optional[str] = ..., num_tickets: _Optional[int] = ...) -> None: ...

class CancelBookingRequest(_message.Message):
    __slots__ = ("event_id", "num_tickets")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    NUM_TICKETS_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    num_tickets: int
    def __init__(self, event_id: _Optional[str] = ..., num_tickets: _Optional[int] = ...) -> None: ...

class BookingResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class ListEventsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListEventsResponse(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[Event]
    def __init__(self, events: _Optional[_Iterable[_Union[Event, _Mapping]]] = ...) -> None: ...
