from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional
import json
from websocket import create_connection
from websocket import WebSocket as W


class AbstractData:
    def __init__(self):
        self.operation = None

    def toJson(self):
        json_data = json.dumps(self, default=lambda o: o.__dict__,
                               sort_keys=True)
        return json_data


class Handler(ABC):
    """
    The StirFryOperator interface declares a method for building the chain of StirFryOperator.
    It also declares a method for executing a request.
    """

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, request) -> Optional[AbstractData]:
        pass


class AbstractHandler(Handler):
    from recipe.models import SubStep

    """
    The default chaining behavior can be implemented inside a base handler
    class.
    """

    _next_handler: Handler = None

    def __init__(self):
        self.operation = 0
        self.__op = {}
        self.ws = None
        self.__connect_ws()

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        # Returning a handler from here will let us link handlers in a
        # convenient way like this:
        # monkey.set_next(squirrel).set_next(dog)
        return handler

    def __connect_ws(self):
        self.ws: W = create_connection("ws://localhost:8000/ws/channel/1/")

    @abstractmethod
    def handle(self, request: SubStep) -> dict | None:
        if self._next_handler:
            return self._next_handler.handle(request)
        return None

    def merge_dictionary(self, x) -> dict:
        return {}
        # self.__op = {
        #     "operation": self.operation
        # }
        # z = x.copy()  # start with keys and values of x
        # z.update(self.__op)  # modifies z with keys and values of y
        # return z
