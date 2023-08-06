# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Pincer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import annotations

from asyncio import get_event_loop, AbstractEventLoop, ensure_future
from platform import system
from typing import Dict, Callable, Awaitable

from websockets import connect
from websockets.exceptions import ConnectionClosedError
from websockets.legacy.client import WebSocketClientProtocol

from pincer import __package__
from pincer._config import GatewayConfig
# TODO: Implement logging
from pincer.core.dispatch import GatewayDispatch
from pincer.core.handlers.heartbeat import handle_hello, handle_heartbeat
from pincer.exceptions import PincerError, InvalidTokenError, \
    UnhandledException

Handler = Callable[[WebSocketClientProtocol, GatewayDispatch], Awaitable[None]]


class Dispatcher:

    """
    The Dispatcher handles all interactions with the discord websocket
    API. This also contains the main event loop, and handles the heartbeat.

    Running the dispatcher will create a connection with the
    Discord WebSocket API on behalf of the provided token. This token
    must be a bot token. (Which can be found on
    `/developers/applications/<bot_id>/bot`)
    """

    # TODO: Add intents argument
    # TODO: Add handlers argument
    def __init__(self, token: str) -> None:
        """
        :param token:
            Bot token for discord's API.
        """

        if len(token) != 59:
            raise InvalidTokenError(
                "Discord Token must have exactly 59 characters."
            )

        self.__token = token
        self.__keep_alive = True

        async def identify_and_handle_hello(socket: WebSocketClientProtocol,
                                            payload: GatewayDispatch):
            """
            Identifies the client to the Discord Websocket API, this
            gets done when the client receives the `hello` (opcode 10)
            message from discord. Right after we send our identification
            the heartbeat starts.

            :param socket:
                The current socket, which can be used to interact
                with the Discord API.

            :param payload: The received payload from Discord.
            """
            await socket.send(str(GatewayDispatch(2, {
                "token": token,
                "intents": 0,
                "properties": {
                    "$os": system(),
                    "$browser": __package__,
                    "$device": __package__
                }
            })))
            await handle_hello(socket, payload)

        self.__dispatch_handlers: Dict[int, Handler] = {
            10: identify_and_handle_hello,
            11: handle_heartbeat
        }

        self.__dispatch_errors: Dict[int, PincerError] = {
            4004: InvalidTokenError()
        }

    async def handler_manager(self, socket: WebSocketClientProtocol,
                              payload: GatewayDispatch,
                              loop: AbstractEventLoop):
        """
        This manages all handles for given OP codes.
        This method gets invoked for every message that is received from
        Discord.

        :param socket:
            The current socket, which can be used to interact
            with the Discord API.
        :param payload: The received payload from Discord.
        :param loop: The current async loop on which the future is bound.
        """
        # TODO: Implement given handlers.
        # TODO: Implement logging
        handler: Handler = self.__dispatch_handlers.get(payload.op)

        if not handler:
            raise UnhandledException(f"Unhandled payload: {payload}")

        ensure_future(handler(socket, payload), loop=loop)

    async def __dispatcher(self, loop: AbstractEventLoop):
        """
        The main event loop.
        This handles all interactions with the websocket API.
        """
        # TODO: Implement logging
        async with connect(GatewayConfig.uri()) as socket:
            while self.__keep_alive:
                try:
                    await self.handler_manager(
                        socket,
                        GatewayDispatch.from_string(await socket.recv()),
                        loop)

                except ConnectionClosedError as exc:
                    self.close()

                    exception = self.__dispatch_errors.get(exc.code)

                    raise exception if exception else UnhandledException(
                        f"Dispatch error ({exc.code}): {exc.reason}")

    def run(self):
        """
        Instantiate the dispatcher, this will create a connection to the
        Discord websocket API on behalf of the client who's token has
        been passed.
        """
        # TODO: Implement logging
        loop = get_event_loop()
        loop.run_until_complete(self.__dispatcher(loop))
        loop.close()

    def close(self):
        """
        Stop the dispatcher from listening and responding to gateway
        events. This should let the client close on itself.
        """
        # TODO: Implement logging
        self.__keep_alive = False
