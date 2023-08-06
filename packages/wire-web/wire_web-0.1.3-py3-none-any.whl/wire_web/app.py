from wire_web.router import Router
from wire_web.request import Request
from wire_web.response import HTMLResponse, Response, PlainTextResponse, JsonResponse
from wire_web.groups import Group
import inspect
import typing


class Wire():
    def __init__(self, strict: bool = True) -> None:
        self.router: Router = Router(strict=strict)

    async def __call__(self, scope: dict, receive, send) -> None:
        req = Request(scope, receive, send)
        try:
            func, params = await self.router.get_handler(req.path, req.method)
            if func:
                if inspect.iscoroutinefunction(func):
                    response: typing.Union[Response, typing.Any] = await func(req, **params)
                    if not isinstance(response, Response):
                        if type(response) == str:
                            response = PlainTextResponse(response, 200)
                        elif type(response) == dict:
                            response = JsonResponse(response, 200)
                    await response(scope, receive, send)
        except Exception as e:
            print(e)
            response = HTMLResponse("Error occured", 404)
            await response(scope, receive, send)

    def get(self, path: str):
        def wrapper(handler: typing.Union[typing.Callable, typing.Awaitable]) -> typing.Union[typing.Callable, typing.Awaitable]:
            self.router.add_route(path, handler, "get")
            return handler
        return wrapper

    def post(self, path: str):
        def wrapper(handler: typing.Union[typing.Callable, typing.Awaitable]) -> typing.Union[typing.Callable, typing.Awaitable]:
            self.router.add_route(path, handler, "post")
            return handler
        return wrapper

    def mount(self, plugin: Group, prefix: str):
        if not prefix.startswith("/"):
            raise Exception(f"Invalid prefix for router {plugin}")
        for route in plugin.routes:
            self.router.add_route(prefix + route[0], route[1], route[2])
        print(f"Mounted router: {plugin}")
        return True
